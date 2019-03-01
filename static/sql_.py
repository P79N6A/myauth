# coding: utf-8
#!/usr/bin/env python
# coding: utf-8


#import pyodbc #sqlserver
import MySQLdb #mysql
import redis #redis
#import cx_Oracle
import os,copy,datetime,time,sys,re
import settings
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#reload(sys)
#sys.setdefaultencoding('utf-8') 
class sqlbase():   
    def getResult(self):  
        rows = [];
        
        columns=[]        
        return rows,columns,{};
    
    def sqlsplit(self,sqlstr,splitstr='go',defaultdatabase=''):
        sqlstr=sqlstr.replace("\r","").decode('utf8')
        sqlstr += "\n"+splitstr;
        
        sqlstrlist=sqlstr.split('\n')
        sqldbi=0
        sqlbuilderlist=[[defaultdatabase,[]]]
        regex_use = re.compile(r'^\s*use\s+\[*(\w+)\]*\s*;*$',re.I) 

        for sqlline in sqlstrlist:
            sqllowerline=sqlline.lower()
            m_use = regex_use.search(sqlline)
            if m_use:
                defaultdatabase=m_use.group(1)
                sqlbuilderlist.append([defaultdatabase,[]])
                sqldbi=sqldbi+1
            elif sqllowerline==splitstr:
                sqlbuilderlist.append([defaultdatabase,[]])
                sqldbi=sqldbi+1
            elif sqllowerline.find(splitstr)==len(sqllowerline)-1:
                sqlbuilderlist[sqldbi][1].append(sqlline[0:-len(splitstr)])
                sqlbuilderlist.append([defaultdatabase,[]])
                sqldbi=sqldbi+1
            else:
                sqlbuilderlist[sqldbi][1].append(sqlline)              
        return sqlbuilderlist
    
    
    
     
class TableFormart_(): 
    def TableFormart(self,rows,columns,formatstr):        
        for formatdict_tmp in formatstr.split('|'):
            formatdict=formatdict_tmp.split(' ')
            formartaction=formatdict[0]
            if 'rowconvert' ==formartaction:
                if len(formatdict)<3:
                    MaxN=9999
                else:
                    MaxN=int(formatdict[2])
                rows,columns=self.TableFormartRowConvert(rows,columns,int(formatdict[1]),MaxN)
            elif 'rowgroup'==formartaction:
                if len(formatdict)<3:
                    sumavg=""
                else:
                    sumavg=formatdict[2]
                rows=self.TableGroup(rows,int(formatdict[1]),sumavg)
            elif 'rowdecreasing'==formartaction:
                if len(formatdict)>=3 and formatdict[2]=='true':
                    isCheckGrowth=True
                else:
                    isCheckGrowth=False
                rows=self.TableFormartRowDecreasing(rows,int(formatdict[1]),isCheckGrowth)
        return rows,columns

    def TableGroup(self,rows,groupi,sumavg):
        newrows=[]
        if groupi==0:
            rowcount=len(rows)
            if rowcount>0:                
                newrow=rows[0];
                columncount=len(newrow);
                #print (rows)
                #print(rowcount)
                #print(columncount)
                for i in range(1,rowcount):
                    for j in range(0,columncount):
                        newrow[j]=newrow[j]+rows[i][j]
            return [newrow]                    
        else:
            return rows;

    #这是个坑，为了实现一种很特殊的行列转换．按groupi提供的列行列转换，并分组合并．暂时只需要sum.另count已经算好了，用sum/count可得avg
    def TableFormartRowConvert(self,rows,columns,groupi,MaxN=9999):
        dic_columns={}
        dic_columns_result={}
        list_columns_result=[]
        row_blank=[] #default blank row
        i_columnleft=groupi
        if groupi>0:
            list_columns_result.extend(columns[0:groupi])
            #row_blank.extend(rows[0][0:groupi]) #time
        i_valuecolunmn=len(columns)-(groupi+2) #muti value columns
        extend_valuecolumn=[]
        if i_valuecolunmn>0:        
            list_columns_result.append('_value_')
            dic_columns_result['_value_']=groupi
            extend_valuecolumn.extend(columns[groupi+1])
            #row_blank.append('')#value1,value2
            i_columnleft+=1
        for row in rows:
            columntype=row[groupi]
            if dic_columns.has_key(columntype):
                dic_columns[columntype]+=row[groupi+1]
            else:
                dic_columns[columntype]=row[groupi+1]
        column_sort=sorted(dic_columns.iteritems(),key=lambda dic_columns:dic_columns[1],reverse=True)
        #print column_sort
        if len(column_sort)>MaxN:
            column_sortlist=list(column_sort[0:MaxN-1])
            column_sortlist.append(('_other_',0)) 
        else:
            column_sortlist=list(column_sort)
        for columni,(columnname,columnvalue) in enumerate(column_sortlist):
            dic_columns_result[columnname]=i_columnleft+columni
            list_columns_result.append(columnname)  
        row_blank = [0]*len(dic_columns_result);
        #ok:
        # dic_columns_result,list_columns_result
        rows_values=[] #sum 
        rows_count=[] #count
        lastrowheader=['_none_']
        rowi=-1
        for row in rows:
            now_rowheader=list(row[0:groupi])
            if i_valuecolunmn>0:
                now_rowheader.append('_none_')
                for p_i in  range(0,i_valuecolunmn+1):
                    now_rowheader[-1]= (columns[i_columnleft+p_i])
                    #print now_rowheader
                    if now_rowheader!=lastrowheader:
                        rowblank_tmp=[]
                        rowblank_tmp.extend(now_rowheader)
                        rowblank_tmp.extend(row_blank)
                        rows_values.append(copy.deepcopy(rowblank_tmp))
                        rows_count.append(copy.deepcopy(rowblank_tmp))
                        rowi+=1
                        lastrowheader=copy.deepcopy(now_rowheader)
                    clumnname_tmp=row[groupi]
                    if dic_columns_result.has_key(clumnname_tmp):
                        columnindex=dic_columns_result[clumnname_tmp]
                    else:
                        columnindex=dic_columns_result['_other_']
                        columnvalue=row[p_i+1+groupi]
                        rows_values[rowi][columnindex]+=columnvalue
                        rows_count[rowi][columnindex]+=1
            else:
                if now_rowheader!=lastrowheader:
                    rowblank_tmp=[]
                    rowblank_tmp.extend(now_rowheader)
                    rowblank_tmp.extend(row_blank)
                    rows_values.append(copy.deepcopy(rowblank_tmp))
                    rows_count.append(copy.deepcopy(rowblank_tmp))
                    rowi+=1
                    lastrowheader=copy.deepcopy(now_rowheader)
                clumnname_tmp=row[groupi]
                #print clumnname_tmp
                if dic_columns_result.has_key(clumnname_tmp):
                    columnindex=dic_columns_result[clumnname_tmp]
                else:
                    columnindex=dic_columns_result['_other_']
                #print rowi,columnindex 
                columnvalue=row[groupi+1]            
                rows_values[rowi][columnindex]+=columnvalue
                rows_count[rowi][columnindex]+=1

        return rows_values,list_columns_result
        #printflist(rows_values)
        #print '!'*50
        #printflist(rows_count)

    #得到递减list
    def TableFormartRowDecreasing(self,row,ValueColumnIndex,isCheckGrowth=False):
        len_rows=len(row)    
        if len_rows<1:
            return row
        columnValueList=range(ValueColumnIndex,len(row[0]))
        #print columnValueList
        new_list=[]
        for i in range(1,len_rows):
            new_row=list(row[i][0:ValueColumnIndex])            
            for j in columnValueList:
                lastvalue=row[i-1][j]
                nowvalue=row[i][j]
                thisvalue=nowvalue-lastvalue
                if isCheckGrowth and thisvalue<0:
                    thisvalue=0
                new_row.append(thisvalue)
            if i==1:
                lastlist=copy.deepcopy(new_row)
                for lindex_last in range(0,ValueColumnIndex):
                    lastlist[lindex_last]=row[0][lindex_last]
                new_list.append(lastlist)

            new_list.append(new_row)
        
        #print new_list
        #print '*'*50
        #print row
        return new_list 

class sqlserver(sqlbase):  
    def __init__(self, connlist,sqlstr,isadmin=0):
        if isadmin==1:
            connlist[2]=settings.sqlserver_admin_user; 
            connlist[3]=settings.sqlserver_admin_password; 
        if isadmin==-1:
            connlist[2]=settings.sqlserver_staff_user; 
            connlist[3]=settings.sqlserver_staff_password;             
        #sqlconnstr="DRIVER=FreeTDS;SERVER=%s;PORT=%s;UID=%s;PWD=%s;DATABASE=%s;TDS_Version=8.0;client charset = UTF-8;connect timeout=10;"%(connlist[0],connlist[1],connlist[2],connlist[3],connlist[4])
        self.connstrlist=connlist
        sqlconnstr=settings.sqlserverdriver%(connlist[0],connlist[1],connlist[2],connlist[3],connlist[4])
        self.conn=pyodbc.connect(sqlconnstr,autocommit=True,ansi=False,unicode_results=True)
  
        #self.conn=pyodbc.connect(sqlconnstr,ansi=False,unicode_results=True)
        self.sqlstr=sqlstr

    def getResultSqlFormat(self,sqlstr,formatstr=""):
        if "maxrow:" in formatstr:
            maxrows=int(formatstr.replace("maxrow:",""))
            rows,columns,select_times=self.getResultSQL(sqlstr,True,maxrows)
        else:
            rows,columns,select_times=self.getResultSQL(sqlstr)
            if(" "  in formatstr):
                rows,columns=TableFormart_().TableFormart(rows,columns,formatstr)
        return rows,columns,select_times

    def getResultSqlmuti(self,sqlstr,formatstr=""):
        resultlist=[]
        sqlstrlist=self.sqlsplit(sqlstr.replace("\ngo","\n;"),";","")
        lastdbname=''
     
        if "maxrow:" in formatstr:
            maxrows=int(formatstr.replace("maxrow:",""))
        else:
            maxrows=9999
        for defaultdbname,sqlstrlist in sqlstrlist:
            if lastdbname!=defaultdbname:
                lastdbname=defaultdbname                
                sqlconnstr=settings.sqlserverdriver%(self.connstrlist[0],self.connstrlist[1],self.connstrlist[2],self.connstrlist[3],defaultdbname)
                self.conn=pyodbc.connect(sqlconnstr,autocommit=True,ansi=False,unicode_results=True)
            if len(sqlstrlist)==0:
                continue
            sqlnewstr="\n".join(sqlstrlist)
            if len(sqlnewstr.replace("\n","").replace(" ",""))<3:
                continue
            resultlist.append(self.getResultSQL(sqlnewstr,False,maxrows))
        self.close()
        return resultlist



    def getResultSQL(self,sqlstr,isautoclose=True,maxrows=9999):
        cursor = self.conn.cursor()

        #sqlstr=sqlstr.decode('GBK')
        step_starttime =time.time()

        cursor.execute(sqlstr)

        #rows = cursor.fetchall()

        rows = cursor.fetchmany(maxrows)

        columns = [t[0].decode('utf8') for t in cursor.description]
        #if len(rows)>9999:
        #    rows=rows[0:9999]

        cursor.close()

        if isautoclose:
            self.conn.close()
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return rows,columns,select_times;


    def getResult(self):        
        return self.getResultSQL(self.sqlstr)
   
    def exe_sql(self,sqlstr,iswait=False):        
        cursor = self.conn.cursor()
        step_starttime =time.time()    
        cursor.execute(sqlstr.decode('utf8'))
        if iswait:
            while cursor.nextset():
                pass
        #self.conn.commit()
        cursor.close()
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return True,select_times

    def exe_sql_para(self,sqlstr,paras,iswait=False):        
        cursor = self.conn.cursor()
        step_starttime =time.time()    
        cursor.execute(sqlstr.decode('utf8'),paras)
        if iswait:
            while cursor.nextset():
                pass
        #self.conn.commit()
        cursor.close()
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return True,select_times

    def exe_sql_para_format(self,sqlstr,paras,formatstr=""):
        dic_return={'formatstr':formatstr}   
        cursor = self.conn.cursor()
        step_starttime =time.time()    
        cursor.execute(sqlstr.decode('utf8'),paras)
        #if("insertid" in formatstr):
        #    dic_return['insertid']=conn.insert_id()
        if("iswait" in formatstr):
            while cursor.nextset():
                pass
        #self.conn.commit()
        cursor.close()
        #print("*****>sql_.py> sqlserver.format")
        #print(dic_return) 
        dic_return['runtimes']=int((time.time()-step_starttime)*1000) 
        return True,dic_return

 


    def close(self):
        try:
            self.conn.close()
        except:
            pass              

class mysql(sqlbase):  
    def __init__(self, connlist,sqlstr,isadmin=0):
        if isadmin==1:
            connlist[2]=settings.mysql_admin_user; 
            connlist[3]=settings.mysql_admin_password; 
        if isadmin==-1:
            connlist[2]=settings.mysql_staff_user; 
            connlist[3]=settings.mysql_staff_password;
        if isadmin==0:
            if connlist[2] in ("dba_auto","","auto"):
                connlist[2]=settings.mysql_normal_user; 
                connlist[3]=settings.mysql_normal_password;    
            self.conn= MySQLdb.connect(connlist[0],port=int(connlist[1]),user=connlist[2], passwd=connlist[3],db=connlist[4],charset="utf8",connect_timeout=5,read_timeout=18000,autocommit =1)
        else:
            self.conn= MySQLdb.connect(connlist[0],port=int(connlist[1]),user=connlist[2], passwd=connlist[3],db=connlist[4],charset="utf8",connect_timeout=5,read_timeout=100,autocommit =1)
        
        self.sqlstr=sqlstr

    def getResultSqlFormat(self,sqlstr,formatstr=""):
        if "maxrow:" in formatstr:
            maxrows=int(formatstr.replace("maxrow:",""))
            rows,columns,select_times=self.getResultSQL(sqlstr,True,maxrows)
        else:
            rows,columns,select_times=self.getResultSQL(sqlstr)
            if(" "  in formatstr):
                rows,columns=TableFormart_().TableFormart(rows,columns,formatstr)
        return list(rows),columns,select_times

    def getResultSqlmuti(self,sqlstr,formatstr=""):
        resultlist=[]
        sqlstrlist=self.sqlsplit(sqlstr,";","")
        lastdbname=''
        if "maxrow:" in formatstr:
            maxrows=int(formatstr.replace("maxrow:",""))
        else:
            maxrows=9999
        for defaultdbname,sqlstrlist in sqlstrlist:
            if lastdbname!=defaultdbname:
                lastdbname=defaultdbname
                self.conn.select_db(defaultdbname)
            if len(sqlstrlist)==0:
                continue
            sqlnewstr="\n".join(sqlstrlist)
            if len(sqlnewstr.replace("\n","").replace(" ",""))<3:
                continue
            resultlist.append(self.getResultSQL(sqlnewstr,False,maxrows))
        self.close()
        return resultlist


    def getResultSQL(self,sqlstr,isautoclose=True,maxrows=9999):  
        cursor = self.conn.cursor()
        step_starttime =time.time()        
        cursor.execute(sqlstr)
        #rows = cursor.fetchall()
        rows = cursor.fetchmany(maxrows)
        columns = [t[0] for t in cursor.description]
        cursor.close()
        if isautoclose:
            self.conn.close()
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return rows,columns,select_times


    def getResultSQL_para(self,sqlstr,para,maxrows=9999):  
        cursor = self.conn.cursor()
        step_starttime =time.time()        
        cursor.execute(sqlstr,para)
        #rows = cursor.fetchall()      
        rows = cursor.fetchmany(maxrows)
        columns = [t[0] for t in cursor.description]
        cursor.close()
        self.conn.close()
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return rows,columns,select_times


    def getResult(self):        
        return self.getResultSQL(self.sqlstr)
    def exe_sql(self,sqlstr,iswait=False):   
        cursor = self.conn.cursor()
        step_starttime =time.time()
        sqlstrlist= sqlstr.split(";")
        for sqlstr_real in sqlstrlist:
            if len(sqlstr_real)>5:                   
                cursor.execute(sqlstr_real)
                if iswait:
                    while cursor.nextset():
                        pass
                self.conn.commit()                
        cursor.close()
        select_times={'select_times':int((time.time()-step_starttime)*1000)}
        #self.conn.close()
        return True,select_times

    def exe_sql_para(self,sqlstr,paras,iswait=False):   
        cursor = self.conn.cursor()
        step_starttime =time.time()
        sqlstrlist= sqlstr.split(";")
        for sqlstr_real in sqlstrlist:
            if len(sqlstr_real)>5:          
                cursor.execute(sqlstr_real,paras)                
                if iswait:
                    while cursor.nextset():
                        pass
                self.conn.commit()
        cursor.close()        
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}  
        return True,select_times

  
    def exe_sql_para_format(self,sqlstr,paras,formatstr=""):
        #print("*****>sql_.py")
        dic_return={'formatstr':formatstr}   
        cursor = self.conn.cursor()
        step_starttime =time.time()
        cursor.execute(sqlstr,paras)
        #print(paras)
        #print(formatstr)
        if("insertid" in formatstr):
            #print("*****>")
            dic_return['insertid']=self.conn.insert_id()
            
        self.conn.commit()
        cursor.close()
        dic_return['runtimes']=int((time.time()-step_starttime)*1000)
        #print("*****>sql_.py")
        #print(dic_return) 
        return True,dic_return

        #cursor.execute("insert into colors(color, abbr) values(%s, %s)", ('blue', 'bl'))

    def close(self):
        try:
            self.conn.close()
        except:
            pass     
      

class redis_Redis(sqlbase):
    def __init__(self, connlist,sqlstr,isadmin=False):  
        if connlist[4]=="":
            self.conn = redis.Redis(host=connlist[0], port=connlist[1], password=connlist[3], db=connlist[4])
        else:
            self.conn = redis.Redis(host=connlist[0], port=connlist[1], db=connlist[4])
        self.sqlstr=sqlstr

    def getResultSqlFormat(self,sqlstr,formatstr):
        if "maxrow:" in formatstr:
            maxrows=int(formatstr.replace("maxrow:",""))
            rows,columns,select_times=self.getResultSQL(sqlstr)
        else:
            rows,columns,select_times=self.getResultSQL(sqlstr)
            if(" "  in formatstr):
                rows,columns=TableFormart_().TableFormart(rows,columns,formatstr)
        return rows,columns,select_times

#region 
    #redis BEGIN
    def redis_keys(self,keys):
        values=self.conn.mget(keys)
        rows=map(list,zip(*[keys,values]))
        columns=['keys','values']
        return rows,columns
    def redis_info(self,keys):
        #print('dd')
        values=self.conn.info()
        rows=[]
        if len(keys)==1 and keys[0] in("*",'info'):
            columns=[]
            for key, value in values.items():
                #if '_human' in key:
                #    continue
                rows.append(value)
                columns.append(key)
        else:
            columns=keys
            for key in keys:
                if key in ('keys','expires','avg_ttl'):
                    if values.has_key('db0'):
                        rows.append(values['db0'].get(key,'0'))
                        continue
                rows.append(values.get(key,'0'))
            #print(rows)
        #print(rows)
        return [rows],columns
    def redis_hash(self,keys):
        rows=[self.conn.hmget(keys[0],keys[1:])]
        columns=keys[1:]
        return rows,columns
    def redis_zrange(self,keys):
        dic_para={}
        for keyi,key in enumerate(keys):
            dic_para[keyi]=key
        rows=self.conn.zrange(dic_para[0],dic_para.get(1,0),dic_para.get(1,9999),False,True)
        columns=['zsortname','zsortvalue']
        return rows,columns
    def redis_smembers(self,keys):
        rows=zip(tuple(self.conn.smembers(keys[0])))
        #print(rows)
        columns=['smembers']
        return rows,columns    
    def redis_empty(self,keys):
        rows=[(keys[0])]
        columns=[""]
        return rows,columns 

    def redis_w_del(self,keys):
        return self.conn.delete(*keys)    

    def redis_w_hset(self,keys):
        if len(keys)>=3:
            #print(keys[0],keys[1],keys[2])
            return self.conn.hset(keys[0],keys[1],keys[2])
            
        return -1

    def redis_w_hsetnx(self,keys):
        if len(keys)>=3:
            return self.conn.hsetnx(keys[0],keys[1],keys[2])
        return -1

    def redis_w_sadd(self,keys):
        if len(keys)>=2:
            return self.conn.sadd(keys[0],*keys[1:])
        return -1
    def redis_w_srem(self,keys):
        if len(keys)>=2:
            return self.conn.srem(keys[0],*keys[1:])
        return -1

    def redis_w_zadd(self,keys):
        if len(keys)>=3:
            return self.conn.zadd(keys[0],*keys[1:]) #name1,score1,name2,score2
        return -1

    def redis_w_zrem(self,keys):
        if len(keys)>=2:
            return self.conn.zrem(keys[0],*keys[1:])
        return -1

#end region
    def getResultSQL(self,sqlstr,isautoclose=True,maxrows=9999):                 
        indexi=sqlstr.index(':')
        #print(indexi)
        if(indexi<2):
            return  [],[],{'runtimes':0}
        sqlaction=sqlstr[0:indexi].replace(" ","").replace("\r","").replace("\n","")
        sqlstr=sqlstr[indexi+1:]
        step_starttime =time.time()    
        keys=sqlstr.split(',')
        #print(keys)
        #print("*"*10)
        if keys.count==0:
            return  [],[],{'runtimes':0}
        redislist = {  
        'keys':self.redis_keys,
        'info':self.redis_info,
        'hash':self.redis_hash,
        'zrange':self.redis_zrange,
        'smembers':self.redis_smembers
        }
        rows,columns = redislist.get(sqlaction,self.redis_empty)(keys);                
        select_times={'runtimes':int((time.time()-step_starttime)*1000)} 
        return rows,columns,select_times

    def getResult(self):        
        return self.getResultSQL(self.sqlstr)
    def exe_sql(self,sqlstr_c,iswait=False): 
        sqlstrlist= sqlstr_c.replace("\r","").split("\n")
        step_starttime =time.time()
        for sqlstr in sqlstrlist:
            if len(sqlstr)>5:  
                indexi=sqlstr.index(':')
                if(indexi<2):
                    continue
                sqlaction=sqlstr[0:indexi].replace(" ","").replace("|n|","\n")
                sqlstr=sqlstr[indexi+1:]                
                keys=sqlstr.split(',')                        
                if keys.count==0:
                    return  False,{'runtimes':99}
                redislist = {         
                'del':self.redis_w_del,  
                'hset':self.redis_w_hset,
                'hsetnx':self.redis_w_hsetnx,
                'sadd':self.redis_w_sadd,
                'srem':self.redis_w_srem,
                'zadd':self.redis_w_zadd,
                'zrem':self.redis_w_zrem 
                }         
                result = redislist.get(sqlaction,self.redis_empty)(keys);                
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}      
        return True,select_times
    def close(self):
        pass        

    def exe_sql_para_format(self,sqlstr,paras,formatstr=""):
        return True,{}



#class oracle(sqlbase):  
#    def __init__(self, connlist,sqlstr,isadmin=0):        
#        #   
#        if isadmin==1:
#            dsn_tns = cx_Oracle.makedsn(connlist[0],connlist[1], connlist[4])
#            self.conn = cx_Oracle.connect(connlist[2], connlist[3], dsn=dsn_tns,mode=cx_Oracle.SYSDBA)
#        else:
#            connstr="%s/%s@%s:%s/%s"%(connlist[2],connlist[3],connlist[0],connlist[1],connlist[4])  
#            self.conn=cx_Oracle.connect(connstr)
#        self.sqlstr=sqlstr

#    def getResultSqlFormat(self,sqlstr,formatstr=""):
#        if "maxrow:" in formatstr:
#            maxrows=int(formatstr.replace("maxrow:",""))
#            rows,columns,select_times=self.getResultSQL(sqlstr,True,maxrows)
#        else:
#            rows,columns,select_times=self.getResultSQL(sqlstr)
#        if(" "  in formatstr):
#            rows,columns=TableFormart_().TableFormart(rows,columns,formatstr)
#        return list(rows),columns,select_times


 

#    def getResultSQL(self,sqlstr,isautoclose=True,maxrows=9999):
#        cursor = self.conn.cursor()
#        step_starttime =time.time()
#        cursor.execute(sqlstr)
#        rows = cursor.fetchall()
#        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
#        columns = [t[0] for t in cursor.description]
#        cursor.close()
#        if isautoclose:
#            self.conn.close()        
#        return rows,columns,select_times


#    def getResultSqlmuti(self,sqlstr,formatstr=""):
#        resultlist=[]
#        sqlstrlist=self.sqlsplit(sqlstr,";","")
#        lastdbname=''
#        for defaultdbname,sqlstrlist in sqlstrlist:
#            if sqlstrlist!=defaultdbname:
#                lastdbname=defaultdbname               
#            if len(sqlstrlist)==0:
#                continue
#            sqlnewstr="\n".join(sqlstrlist)
#            if len(sqlnewstr.replace("\n","").replace(" ",""))<3:
#                continue
#            resultlist.append(self.getResultSQL(sqlnewstr))
#        return resultlist


#    def getResultSQL_para(self,sqlstr,para,maxrows=9999):  
#        cursor = self.conn.cursor()
#        step_starttime =time.time()        
#        cursor.execute(sqlstr,para)
#        rows = cursor.fetchmany(maxrows)
#        columns = [t[0] for t in cursor.description]
#        cursor.close()
#        self.conn.close()
#        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
#        return rows,columns,select_times

        
#    def getResult(self):        
#        return self.getResultSQL(self.sqlstr)
#    def exe_sql(self,sqlstr,iswait=False): 
#        return True 

#    def exe_sql_para(self,sqlstr,paras,iswait=False):
#        return True 
#    def exe_sql_para_format(self,sqlstr,paras,formatstr=""):
#        return True     
#    def close(self):
#        try:
#            self.conn.close()
#        except:
#            pass



class url(sqlbase):  
    def __init__(self, connlist,sqlstr,isadmin=0):  
        self.url=connlist[0]
        self.postdata=connlist[1]
        self.dataset=connlist[2]
        self.cookieid=connlist[3]
        self.regs=sqlstr
    def getResultSqlFormat(self,sqlstr,formatstr):
        rows,columns,select_times=self.getResultSQL(sqlstr)
        if(" "  in formatstr):
            rows,columns=TableFormart_().TableFormart(rows,columns,formatstr)
        return rows,columns,select_times

    def getResultSQL(self,regs):
        #if len(self.dataset)>0:
            #得到dataset结果循环
        step_starttime =time.time()
        str= fx.get(self.url)
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        rows,columns=fx.getRegTable(regs,str,iscolumns)        
        return rows,columns,select_times
        
    def getResult(self):        
        return self.getResultSQL(self.regs)

    def exe_sql(self,sqlstr,iswait=False): 
        step_starttime =time.time()
        fx.get(self.url)
        select_times={'runtimes':int((time.time()-step_starttime)*1000)}
        return True 

    def close(self):
        pass
              
       #fx=net_.net_()
       # str= fx.post("sag/Site/Login", "username={0}&password={1}")
       # #str= fx.get("/sag/Aos/Index#")
       # tplData={"html":str}
       # render=web.template.frender('templates/top-test.htm')
class sql():  
    @staticmethod  
    def createFacsql(sqltype,connstr,sqlstr=" ",isadmin=0): 
        #connstr= connstr.replace("@f",';').replace("@d",'='); 
        #print connstr
        #print '!'*50
        connlist=connstr.split(';')
        if sqltype<>"url":  
            assert(len(connlist)>=5)

        optList = {  
        'sqlserver':sqlserver,  
        'mysql':mysql,  
        'redis':redis_Redis
        #'oracle':oracle        
        }
        ooo = sqlbase()  
        if(optList.has_key(sqltype)):  
            ooo = optList[sqltype](connlist,sqlstr,isadmin);          
        return ooo 


if __name__ == "__main__":
    l1=[(1,'a'),(2,'b'),(3,'c')]
    l2=[(1,0,0),(2,0,0),(3,0,0)]
    #print(zip(l1, l2))
    #step_starttime =time.time()
    #for i in range(5000):
        #l3=map(lambda x: x[0]+x[1], zip(l1, l2))
    l3=[(1,'a')+x for x in l2]
        #l3=[]
        #for i,t in enumerate(l2):
        #    l3.append(l1[i]+t)

    #print (time.time()-step_starttime)
    #print(l3)
    #print(l3)
    #host=connlist[0], port=connlist[1], password=connlist[3], db=connlist[4]
    #r=redis_Redis(("172.21.28.105",1738,"","","0"),"")
    #str=r.getResultSQL("hash:admin_report:dcfq7wtkujyoxgear023b4in5z,title")
    #print(str[0][0][0].decode('utf8'))
    pass      
