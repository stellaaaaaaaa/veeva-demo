from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PageList(db.Model):
    __tablename__ = 'page_lists'
    ID = db.Column(db.String(32), primary_key=True)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    DELETED = db.Column(db.String(1))

    # 关系定义（与 page_list_fields 一对多）
    page_list_fields = db.relationship('PageListField', backref='page_list', lazy=True)
    page_layouts = db.relationship('PageLayout', backref='page_list', lazy=True)


class Object(db.Model):
    __tablename__ = 'objects'
    ID = db.Column(db.String(32), primary_key=True)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    TABLE_NAME = db.Column(db.String(255))
    DELETED = db.Column(db.String(1))

    # 关系定义（与 object_fields 一对多）
    object_fields = db.relationship('ObjectField', backref='object', lazy=True)


class ObjectField(db.Model):
    __tablename__ = 'object_fields'
    ID = db.Column(db.String(32), primary_key=True)
    OBJECT_ID = db.Column(db.String(32), db.ForeignKey('objects.ID'), nullable=False)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1))

    # 关系定义（与 page_list_fields 和 page_layout_fields 一对多）
    page_list_fields = db.relationship('PageListField', backref='object_field', lazy=True)
    page_layout_fields = db.relationship('PageLayoutField', backref='object_field', lazy=True)


class PageListField(db.Model):
    __tablename__ = 'page_list_fields'
    ID = db.Column(db.String(32), primary_key=True)
    NAME = db.Column(db.String(255))
    OBJECT_FIELD_ID = db.Column(db.String(32), db.ForeignKey('object_fields.ID'), nullable=False)
    PAGE_LIST_ID = db.Column(db.String(32), db.ForeignKey('page_lists.ID'), nullable=False)
    HIDDEN = db.Column(db.String(1))
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1))

    # 外键约束
    object_field = db.relationship('ObjectField', backref='page_list_fields')
    page_list = db.relationship('PageList', backref='page_list_fields')


class PageLayout(db.Model):
    __tablename__ = 'page_layouts'
    ID = db.Column(db.String(32), primary_key=True)
    NAME = db.Column(db.String(255))
    PAGE_LIST_ID = db.Column(db.String(32), db.ForeignKey('page_lists.ID'), nullable=False)
    DELETED = db.Column(db.String(1))

    # 外键约束
    page_list = db.relationship('PageList', backref='page_layouts')


class PageLayoutField(db.Model):
    __tablename__ = 'page_layout_fields'
    ID = db.Column(db.String(255), primary_key=True)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    PAGE_LAYOUT_ID = db.Column(db.String(32), db.ForeignKey('page_layouts.ID'), nullable=False)
    OBJECT_FIELD_ID = db.Column(db.String(32), db.ForeignKey('object_fields.ID'), nullable=False)
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1))

    # 外键约束
    page_layout = db.relationship('PageLayout', backref='page_layout_fields')
    object_field = db.relationship('ObjectField', backref='page_layout_fields')
