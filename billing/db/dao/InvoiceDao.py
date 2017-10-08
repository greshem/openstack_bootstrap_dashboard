# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
发票数据库操作类
'''
from billing.db.object.models import Invoice
from billing.db.sqlalchemy import session as sa
from billing.db.Pagination import Pagination
from billing.constant.sql import SQL

class InvoiceDao():
    def __init__(self, invoice=None):
        self.invoice = invoice
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Invoice)
    
    def add(self, session=None):
        if not session:
            session = sa.get_session()
        session.add(self.invoice)
        session.flush()
        self.invoice.address
    
    def update(self, values, session=None):
        if not session:
            session = sa.get_session()
        session.begin()
        self.invoice = session.query(Invoice).filter(Invoice.invoice_id == self.invoice.invoice_id).first()
        values={key:values[key] for key in values.keys() if key not in ('account_id')}
        self.invoice.update(values)
        session.commit()
        self.invoice.address
    
    def detail(self, session=None):
        if not session:
            session = sa.get_session()
        self.invoice = session.query(Invoice).filter(Invoice.invoice_id == self.invoice.invoice_id).first()
        self.invoice.address
        return self.invoice
    
    
    def getInvoiceByPage(self,condition=None, page_no=1, page_size=15, edge_size=0, session=None):
        ''' 分页查询'''
        if not session:
            session = sa.get_session()
        query = session.query(Invoice)
        if condition:
            for (attr, attrValue) in [(key, value)for (key, value) in condition.items()]:
                if attr == 'account_id':
                    query = query.filter(Invoice.account_id == attrValue)
                if attr == 'type':
                    query = query.filter(Invoice.type == attrValue)
                if attr == 'status':
                    query = query.filter(Invoice.status == attrValue)
        pagination = Pagination(query)
        result= pagination.paginate(page_no, page_size, edge_size)
        if result:
            for invoice in result:
                invoice.address
        return result
        
    def getBillAmountSummary(self, account_id, session=None):
        '''可开发票'''
        if not session:
            session = sa.get_session()
        query = session.execute(SQL.getRechargeSummary, {'account_id': account_id})
        rows=query.fetchall()
        d=dict(rows[0])
        session.close()
        return d

    # added by zhangaw
    def getInvoiceNumber(self,account_id,session=None):
        '''发票总数 与 未处理发票数'''
        if not session:
            session=sa.get_session()
        query=session.execute(SQL.invoiceNumberSql,{'account_id':account_id})
        row=query.first()
        invoiceNumDict=dict(row)
        session.close()
        return invoiceNumDict

    def getInvoiceManageDetail(self,condition=None, page_no=1, page_size=5, edge_size=0, session=None):
        '''发票管理列表详情'''
        if not session:
            session = sa.get_session()
        query = session.query(Invoice)
        if condition:
            for (attr, attrValue) in [(key, value)for (key, value) in condition.items()]:
                if attr == 'account_id':
                    query = query.filter(Invoice.account_id == attrValue)
                if attr == 'type':
                    query = query.filter(Invoice.type == attrValue)
                if attr == 'status':
                    query = query.filter(Invoice.status == attrValue)
                if attr == 'titlelike':
                    query = query.filter(Invoice.title.like('%' + attrValue.replace('_','\_') + '%'))
        pagination = Pagination(query)
        result= pagination.paginate(page_no, page_size, edge_size)
        if result:
            for invoice in result:
                invoice.address
        return result
    # end edit



if __name__=='__main__':
    invoice=InvoiceDao()
    print invoice.getInvoiceNumber('296a6abc-9052-4d01-8632-79ef742e9412')
        

