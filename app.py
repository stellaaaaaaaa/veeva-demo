# app.py
from flask import Flask, request, jsonify
from config import Config
from models import db, PageList, Object, ObjectField, PageListField, PageLayout, PageLayoutField
import uuid

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 在应用上下文中创建所有表（仅首次运行时）
with app.app_context():
    db.create_all()


# ---------------------------
# PageList API
# ---------------------------
@app.route('/page_lists', methods=['GET'])
def get_page_lists():
    pages = PageList.query.filter_by(DELETED='0').all()
    result = [{'ID': p.ID, 'NAME': p.NAME, 'LABEL': p.LABEL} for p in pages]
    return jsonify(result)


@app.route('/page_list', methods=['POST'])
def create_page_list():
    data = request.get_json()
    page = PageList(
        NAME=data[0].get('NAME'),
        LABEL=data[0].get('LABEL')
    )
    db.session.add(page)
    db.session.commit()
    return jsonify({'message': 'PageList created', 'ID': page.ID}), 201


@app.route('/page_list/<id>', methods=['GET'])
def get_page_list(id):
    page = PageList.query.filter_by(ID=id, DELETED='0').first()
    if page:
        return jsonify({'ID': page.ID, 'NAME': page.NAME, 'LABEL': page.LABEL})
    return jsonify({'message': 'PageList not found'}), 404


@app.route('/page_list/<id>', methods=['PUT'])
def update_page_list(id):
    data = request.get_json()
    page = PageList.query.filter_by(ID=id, DELETED='0').first()
    if not page:
        return jsonify({'message': 'PageList not found or deleted'}), 404
    page.NAME = data[0].get('NAME', page.NAME)
    page.LABEL = data[0].get('LABEL', page.LABEL)
    db.session.commit()
    return jsonify({'message': 'PageList updated'})


@app.route('/page_list/<id>', methods=['DELETE'])
def soft_delete_page_list(id):
    page = PageList.query.filter_by(ID=id, DELETED='0').first()
    if not page:
        return jsonify({'message': 'PageList not found or already deleted'}), 404
    page.cascade_soft_delete()  # 调用集中处理的级联软删除
    db.session.commit()
    return jsonify({'message': 'PageList and related records soft deleted'})


@app.route('/page_list/restore/<id>', methods=['PUT'])
def restore_page_list(id):
    page = PageList.query.filter_by(ID=id, DELETED='1').first()
    if not page:
        return jsonify({'message': 'PageList not found or not deleted'}), 404
    page.cascade_restore()  # 级联恢复
    db.session.commit()
    return jsonify({'message': 'PageList and related records restored'})


@app.route('/page_list/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_page_list(id):
    page = PageList.query.filter_by(ID=id).first()
    if not page:
        return jsonify({'message': 'PageList not found'}), 404
    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': 'PageList permanently deleted'})


# ---------------------------
# Object API
# ---------------------------
@app.route('/objects', methods=['GET'])
def get_objects():
    objs = Object.query.filter_by(DELETED='0').all()
    result = [{'ID': o.ID, 'NAME': o.NAME, 'LABEL': o.LABEL, 'TABLE_NAME': o.TABLE_NAME} for o in objs]
    return jsonify(result)


@app.route('/object', methods=['POST'])
def create_object():
    data = request.get_json()
    obj = Object(
        NAME=data[0].get('NAME'),
        LABEL=data[0].get('LABEL'),
        TABLE_NAME=data[0].get('TABLE_NAME')
    )
    db.session.add(obj)
    db.session.commit()
    return jsonify({'message': 'Object created', 'ID': obj.ID}), 201


@app.route('/object/<id>', methods=['GET'])
def get_object(id):
    obj = Object.query.filter_by(ID=id, DELETED='0').first()
    if obj:
        return jsonify({'ID': obj.ID, 'NAME': obj.NAME, 'LABEL': obj.LABEL, 'TABLE_NAME': obj.TABLE_NAME})
    return jsonify({'message': 'Object not found'}), 404


@app.route('/object/<id>', methods=['PUT'])
def update_object(id):
    data = request.get_json()
    obj = Object.query.filter_by(ID=id, DELETED='0').first()
    if not obj:
        return jsonify({'message': 'Object not found or deleted'}), 404
    obj.NAME = data[0].get('NAME', obj.NAME)
    obj.LABEL = data[0].get('LABEL', obj.LABEL)
    obj.TABLE_NAME = data[0].get('TABLE_NAME', obj.TABLE_NAME)
    db.session.commit()
    obj = Object.query.filter_by(ID=id, DELETED='0').first()
    return jsonify({'message': 'Object updated','ID': obj.ID, 'NAME': obj.NAME, 'LABEL': obj.LABEL, 'TABLE_NAME': obj.TABLE_NAME})


@app.route('/object/<id>', methods=['DELETE'])
def soft_delete_object(id):
    obj = Object.query.filter_by(ID=id, DELETED='0').first()
    if not obj:
        return jsonify({'message': 'Object not found or already deleted'}), 404
    obj.cascade_soft_delete()
    db.session.commit()
    return jsonify({'message': 'Object and its related fields soft deleted'})


@app.route('/object/restore/<id>', methods=['PUT'])
def restore_object(id):
    obj = Object.query.filter_by(ID=id, DELETED='1').first()
    if not obj:
        return jsonify({'message': 'Object not found or not deleted'}), 404
    obj.cascade_restore()
    db.session.commit()
    return jsonify({'message': 'Object and its related fields restored'})


@app.route('/object/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_object(id):
    obj = Object.query.filter_by(ID=id).first()
    if not obj:
        return jsonify({'message': 'Object not found'}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({'message': 'Object permanently deleted'})


# ---------------------------
# ObjectField API
# ---------------------------
@app.route('/object_fields', methods=['GET'])
def get_object_fields():
    fields = ObjectField.query.filter_by(DELETED='0').all()
    result = [{'ID': f.ID, 'OBJECT_ID': f.OBJECT_ID, 'NAME': f.NAME, 'LABEL': f.LABEL, 'TYPE': f.TYPE} for f in fields]
    return jsonify(result)


@app.route('/object_field', methods=['POST'])
def create_object_field():
    data = request.get_json()
    field = ObjectField(
        OBJECT_ID=data[0].get('OBJECT_ID'),
        NAME=data[0].get('NAME'),
        LABEL=data[0].get('LABEL'),
        TYPE=data[0].get('TYPE')
    )
    db.session.add(field)
    db.session.commit()
    return jsonify({'message': 'ObjectField created', 'ID': field.ID}), 201


@app.route('/object_field/<id>', methods=['GET'])
def get_object_field(id):
    field = ObjectField.query.filter_by(ID=id, DELETED='0').first()
    if field:
        return jsonify({'ID': field.ID, 'OBJECT_ID': field.OBJECT_ID, 'NAME': field.NAME, 'LABEL': field.LABEL, 'TYPE': field.TYPE})
    return jsonify({'message': 'ObjectField not found'}), 404


@app.route('/object_field/<id>', methods=['PUT'])
def update_object_field(id):
    data = request.get_json()
    field = ObjectField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'ObjectField not found or deleted'}), 404
    field.NAME = data[0].get('NAME', field.NAME)
    field.LABEL = data[0].get('LABEL', field.LABEL)
    field.TYPE = data[0].get('TYPE', field.TYPE)
    db.session.commit()
    # return jsonify({'message': 'ObjectField updated'})
    obj_field = ObjectField.query.filter_by(ID=id, DELETED='0').first()
    return jsonify({'message': 'Object_field updated','ID': obj_field.ID, 'OBJECT_ID': obj_field.OBJECT_ID,'NAME': obj_field.NAME, 'LABEL': obj_field.LABEL, 'TYPE': obj_field.TYPE})




@app.route('/object_field/<id>', methods=['DELETE'])
def soft_delete_object_field(id):
    field = ObjectField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'ObjectField not found or already deleted'}), 404
    field.cascade_soft_delete()
    db.session.commit()
    return jsonify({'message': 'ObjectField soft deleted'})


@app.route('/object_field/restore/<id>', methods=['PUT'])
def restore_object_field(id):
    field = ObjectField.query.filter_by(ID=id, DELETED='1').first()
    if not field:
        return jsonify({'message': 'ObjectField not found or not deleted'}), 404
    field.cascade_restore()
    db.session.commit()
    return jsonify({'message': 'ObjectField restored'})


@app.route('/object_field/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_object_field(id):
    field = ObjectField.query.filter_by(ID=id).first()
    if not field:
        return jsonify({'message': 'ObjectField not found'}), 404
    db.session.delete(field)
    db.session.commit()
    return jsonify({'message': 'ObjectField permanently deleted'})


# ---------------------------
# PageListField API
# ---------------------------
@app.route('/page_list_fields', methods=['GET'])
def get_page_list_fields():
    fields = PageListField.query.filter_by(DELETED='0').all()
    result = [{'ID': f.ID, 'NAME': f.NAME, 'OBJECT_FIELD_ID': f.OBJECT_FIELD_ID, 'PAGE_LIST_ID': f.PAGE_LIST_ID} for f in fields]
    return jsonify(result)


@app.route('/page_list_field', methods=['POST'])
def create_page_list_field():
    data = request.get_json()
    field = PageListField(
        NAME=data[0].get('NAME'),
        OBJECT_FIELD_ID=data[0].get('OBJECT_FIELD_ID'),
        PAGE_LIST_ID=data[0].get('PAGE_LIST_ID'),
        HIDDEN=data[0].get('HIDDEN'),
        TYPE=data[0].get('TYPE')
    )
    db.session.add(field)
    db.session.commit()
    return jsonify({'message': 'PageListField created', 'ID': field.ID}), 201


@app.route('/page_list_field/<id>', methods=['GET'])
def get_page_list_field(id):
    field = PageListField.query.filter_by(ID=id, DELETED='0').first()
    if field:
        return jsonify({'ID': field.ID, 'NAME': field.NAME, 'OBJECT_FIELD_ID': field.OBJECT_FIELD_ID, 'PAGE_LIST_ID': field.PAGE_LIST_ID})
    return jsonify({'message': 'PageListField not found'}), 404


@app.route('/page_list_field/<id>', methods=['PUT'])
def update_page_list_field(id):
    data = request.get_json()
    field = PageListField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'PageListField not found or deleted'}), 404
    field.NAME = data[0].get('NAME', field.NAME)
    field.HIDDEN = data[0].get('HIDDEN', field.HIDDEN)
    field.TYPE = data[0].get('TYPE', field.TYPE)
    db.session.commit()
    return jsonify({'message': 'PageListField updated'})


@app.route('/page_list_field/<id>', methods=['DELETE'])
def soft_delete_page_list_field(id):
    field = PageListField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'PageListField not found or already deleted'}), 404
    field.cascade_soft_delete()
    db.session.commit()
    return jsonify({'message': 'PageListField soft deleted'})


@app.route('/page_list_field/restore/<id>', methods=['PUT'])
def restore_page_list_field(id):
    field = PageListField.query.filter_by(ID=id, DELETED='1').first()
    if not field:
        return jsonify({'message': 'PageListField not found or not deleted'}), 404
    field.cascade_restore()
    db.session.commit()
    return jsonify({'message': 'PageListField restored'})


@app.route('/page_list_field/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_page_list_field(id):
    field = PageListField.query.filter_by(ID=id).first()
    if not field:
        return jsonify({'message': 'PageListField not found'}), 404
    db.session.delete(field)
    db.session.commit()
    return jsonify({'message': 'PageListField permanently deleted'})


# ---------------------------
# PageLayout API
# ---------------------------
@app.route('/page_layouts', methods=['GET'])
def get_page_layouts():
    layouts = PageLayout.query.filter_by(DELETED='0').all()
    result = [{'ID': l.ID, 'NAME': l.NAME, 'PAGE_LIST_ID': l.PAGE_LIST_ID} for l in layouts]
    return jsonify(result)


@app.route('/page_layout', methods=['POST'])
def create_page_layout():
    data = request.get_json()
    layout = PageLayout(
        NAME=data[0].get('NAME'),
        PAGE_LIST_ID=data[0].get('PAGE_LIST_ID')
    )
    db.session.add(layout)
    db.session.commit()
    return jsonify({'message': 'PageLayout created', 'ID': layout.ID}), 201


@app.route('/page_layout/<id>', methods=['GET'])
def get_page_layout(id):
    layout = PageLayout.query.filter_by(ID=id, DELETED='0').first()
    if layout:
        return jsonify({'ID': layout.ID, 'NAME': layout.NAME, 'PAGE_LIST_ID': layout.PAGE_LIST_ID})
    return jsonify({'message': 'PageLayout not found'}), 404


@app.route('/page_layout/<id>', methods=['PUT'])
def update_page_layout(id):
    data = request.get_json()
    layout = PageLayout.query.filter_by(ID=id, DELETED='0').first()
    if not layout:
        return jsonify({'message': 'PageLayout not found or deleted'}), 404
    layout.NAME = data[0].get('NAME', layout.NAME)
    db.session.commit()
    return jsonify({'message': 'PageLayout updated'})


@app.route('/page_layout/<id>', methods=['DELETE'])
def soft_delete_page_layout(id):
    layout = PageLayout.query.filter_by(ID=id, DELETED='0').first()
    if not layout:
        return jsonify({'message': 'PageLayout not found or already deleted'}), 404
    layout.cascade_soft_delete()
    db.session.commit()
    return jsonify({'message': 'PageLayout and its related records soft deleted'})


@app.route('/page_layout/restore/<id>', methods=['PUT'])
def restore_page_layout(id):
    layout = PageLayout.query.filter_by(ID=id, DELETED='1').first()
    if not layout:
        return jsonify({'message': 'PageLayout not found or not deleted'}), 404
    layout.cascade_restore()
    db.session.commit()
    return jsonify({'message': 'PageLayout and its related records restored'})


@app.route('/page_layout/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_page_layout(id):
    layout = PageLayout.query.filter_by(ID=id).first()
    if not layout:
        return jsonify({'message': 'PageLayout not found'}), 404
    db.session.delete(layout)
    db.session.commit()
    return jsonify({'message': 'PageLayout permanently deleted'})


# ---------------------------
# PageLayoutField API
# ---------------------------
@app.route('/page_layout_fields', methods=['GET'])
def get_page_layout_fields():
    fields = PageLayoutField.query.filter_by(DELETED='0').all()
    result = [{'ID': f.ID, 'NAME': f.NAME, 'LABEL': f.LABEL, 'PAGE_LAYOUT_ID': f.PAGE_LAYOUT_ID, 'OBJECT_FIELD_ID': f.OBJECT_FIELD_ID} for f in fields]
    return jsonify(result)


@app.route('/page_layout_field', methods=['POST'])
def create_page_layout_field():
    data = request.get_json()
    field = PageLayoutField(
        NAME=data[0].get('NAME'),
        LABEL=data[0].get('LABEL'),
        PAGE_LAYOUT_ID=data[0].get('PAGE_LAYOUT_ID'),
        OBJECT_FIELD_ID=data[0].get('OBJECT_FIELD_ID'),
        TYPE=data[0].get('TYPE')
    )
    db.session.add(field)
    db.session.commit()
    return jsonify({'message': 'PageLayoutField created', 'ID': field.ID}), 201


@app.route('/page_layout_field/<id>', methods=['GET'])
def get_page_layout_field(id):
    field = PageLayoutField.query.filter_by(ID=id, DELETED='0').first()
    if field:
        return jsonify({'ID': field.ID, 'NAME': field.NAME, 'LABEL': field.LABEL, 'PAGE_LAYOUT_ID': field.PAGE_LAYOUT_ID, 'OBJECT_FIELD_ID': field.OBJECT_FIELD_ID})
    return jsonify({'message': 'PageLayoutField not found'}), 404


@app.route('/page_layout_field/<id>', methods=['PUT'])
def update_page_layout_field(id):
    data = request.get_json()
    field = PageLayoutField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'PageLayoutField not found or deleted'}), 404
    field.NAME = data[0].get('NAME', field.NAME)
    field.LABEL = data[0].get('LABEL', field.LABEL)
    field.TYPE = data[0].get('TYPE', field.TYPE)
    db.session.commit()
    return jsonify({'message': 'PageLayoutField updated'})


@app.route('/page_layout_field/<id>', methods=['DELETE'])
def soft_delete_page_layout_field(id):
    field = PageLayoutField.query.filter_by(ID=id, DELETED='0').first()
    if not field:
        return jsonify({'message': 'PageLayoutField not found or already deleted'}), 404
    field.cascade_soft_delete()
    db.session.commit()
    return jsonify({'message': 'PageLayoutField soft deleted'})


@app.route('/page_layout_field/restore/<id>', methods=['PUT'])
def restore_page_layout_field(id):
    field = PageLayoutField.query.filter_by(ID=id, DELETED='1').first()
    if not field:
        return jsonify({'message': 'PageLayoutField not found or not deleted'}), 404
    field.cascade_restore()
    db.session.commit()
    return jsonify({'message': 'PageLayoutField restored'})


@app.route('/page_layout_field/permanent_delete/<id>', methods=['DELETE'])
def permanent_delete_page_layout_field(id):
    field = PageLayoutField.query.filter_by(ID=id).first()
    if not field:
        return jsonify({'message': 'PageLayoutField not found'}), 404
    db.session.delete(field)
    db.session.commit()
    return jsonify({'message': 'PageLayoutField permanently deleted'})


if __name__ == '__main__':
    app.run(debug=True)
