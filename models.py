# models.py
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PageList(db.Model):
    __tablename__ = 'page_lists'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    DELETED = db.Column(db.String(1), default='0')

    # 关系
    page_list_fields = db.relationship('PageListField', backref='page_list', lazy=True)
    page_layouts = db.relationship('PageLayout', backref='page_list', lazy=True)

    def cascade_soft_delete(self):
        self.DELETED = '1'
        for plf in self.page_list_fields:
            if plf.DELETED != '1':
                plf.cascade_soft_delete()
        for layout in self.page_layouts:
            if layout.DELETED != '1':
                layout.cascade_soft_delete()

    def cascade_restore(self):
        self.DELETED = '0'
        for plf in self.page_list_fields:
            if plf.DELETED != '0':
                plf.cascade_restore()
        for layout in self.page_layouts:
            if layout.DELETED != '0':
                layout.cascade_restore()


class Object(db.Model):
    __tablename__ = 'objects'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    TABLE_NAME = db.Column(db.String(255))
    DELETED = db.Column(db.String(1), default='0')

    object_fields = db.relationship('ObjectField', backref='object', lazy=True)

    def cascade_soft_delete(self):
        self.DELETED = '1'
        for field in self.object_fields:
            if field.DELETED != '1':
                field.cascade_soft_delete()

    def cascade_restore(self):
        self.DELETED = '0'
        for field in self.object_fields:
            if field.DELETED != '0':
                field.cascade_restore()


class ObjectField(db.Model):
    __tablename__ = 'object_fields'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    OBJECT_ID = db.Column(db.String(32), db.ForeignKey('objects.ID'), nullable=False)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1), default='0')

    page_list_fields = db.relationship('PageListField', backref='object_field', lazy=True)
    page_layout_fields = db.relationship('PageLayoutField', backref='object_field', lazy=True)

    def cascade_soft_delete(self):
        self.DELETED = '1'
        for plf in self.page_list_fields:
            if plf.DELETED != '1':
                plf.cascade_soft_delete()
        for plf in self.page_layout_fields:
            if plf.DELETED != '1':
                plf.cascade_soft_delete()

    def cascade_restore(self):
        self.DELETED = '0'
        for plf in self.page_list_fields:
            if plf.DELETED != '0':
                plf.cascade_restore()
        for plf in self.page_layout_fields:
            if plf.DELETED != '0':
                plf.cascade_restore()


class PageListField(db.Model):
    __tablename__ = 'page_list_fields'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    NAME = db.Column(db.String(255))
    OBJECT_FIELD_ID = db.Column(db.String(32), db.ForeignKey('object_fields.ID'), nullable=False)
    PAGE_LIST_ID = db.Column(db.String(32), db.ForeignKey('page_lists.ID'), nullable=False)
    HIDDEN = db.Column(db.String(1))
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1), default='0')

    def cascade_soft_delete(self):
        self.DELETED = '1'

    def cascade_restore(self):
        self.DELETED = '0'


class PageLayout(db.Model):
    __tablename__ = 'page_layouts'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    NAME = db.Column(db.String(255))
    PAGE_LIST_ID = db.Column(db.String(32), db.ForeignKey('page_lists.ID'), nullable=False)
    DELETED = db.Column(db.String(1), default='0')

    page_layout_fields = db.relationship('PageLayoutField', backref='page_layout', lazy=True)

    def cascade_soft_delete(self):
        self.DELETED = '1'
        for field in self.page_layout_fields:
            if field.DELETED != '1':
                field.cascade_soft_delete()

    def cascade_restore(self):
        self.DELETED = '0'
        for field in self.page_layout_fields:
            if field.DELETED != '0':
                field.cascade_restore()


class PageLayoutField(db.Model):
    __tablename__ = 'page_layout_fields'
    ID = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    NAME = db.Column(db.String(255))
    LABEL = db.Column(db.String(255))
    PAGE_LAYOUT_ID = db.Column(db.String(32), db.ForeignKey('page_layouts.ID'), nullable=False)
    OBJECT_FIELD_ID = db.Column(db.String(32), db.ForeignKey('object_fields.ID'), nullable=False)
    TYPE = db.Column(db.String(255))
    DELETED = db.Column(db.String(1), default='0')

    def cascade_soft_delete(self):
        self.DELETED = '1'

    def cascade_restore(self):
        self.DELETED = '0'
