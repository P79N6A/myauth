# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from pub_def import login_required, replace_chart, mana_login, get_random_str
import pub_def
import fmt_html.bui
import fmt_html.jschart
import fmt_html.form_
import redis
import time
import MySQLdb
#from django.db import connection
import simplejson
from collections import OrderedDict
import bcrypt
import string
import random


def homepage(request):
    return render(request, "hi.html")


def hello(request):
    context = {}
    context['hello'] = 'Hello World !~'
    return render(request, 'hello.html', context)


class Inputs:
    def __init__(self, name, title, inputtype="input", desc="", style={}):
        self.name = name
        self.title = title
        self.desc = desc
        self.inputtype = inputtype
        self.style = style

        # self.defaultvalue=defaultvalue

    def toHtml(self, newvalue, islable=True):

        form_ = fmt_html.form_.form_()
        if islable:
            return form_.make_lable(self.title, newvalue)
        else:
            if self.inputtype == "input":
                # paraid,title="",defaultvalue="",spanclass="span8",datatip="input-normal",inputclass="",datarules="",desc=""):
                return form_.make_input(self.name, self.title, newvalue, self.style.get("div-class", ""), self.style.get("data-tip", ""), self.style.get("input-class", ""), self.style.get("data-rules", ""), self.desc)
            elif self.inputtype == "select":
                if self.style.has_key("connstr"):
                    rowlist = []
                elif self.style.has_key("items"):
                    rowlist = self.style.get("items", [])
                else:
                    rowlist = []
                return form_.make_select(self.name, self.title, newvalue, self.style.get("div-class", ""), "input-normal", self.style.get("input-class", ""), rowlist, self.desc)
            elif self.inputtype == "multiselect":
                if self.style.has_key("connstr"):
                    rowlist = []
                elif self.style.has_key("items"):
                    rowlist = self.style.get("items", [])
                else:
                    rowlist = []
                return form_.make_multi_select(self.name, self.title, newvalue, self.style.get("div-class", ""), "input-normal", self.style.get("input-class", ""), rowlist, self.desc)
            elif self.inputtype == "datetime":
                return ""


oo_ms = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("MS - 开发人员", "MS - 开发人员"),
                            ("MS - 兼职模块", "MS - 兼职模块"),
                            ("MS - 产品组", "MS - 产品组"),
                            ("MS - 运营配置模块", "MS - 运营配置模块"),
                            ("商品数据管理员", "商品数据管理员"),
                            ("MS - 采销", "MS - 采销"),
                            ("兼职管理", "兼职管理"),
                            ("MS－客服", "MS－客服"),
                            ("MS-活动管理", "MS-活动管理"),
                            ("MS - 售后模块", "MS - 售后模块"),
                            ("MS－财务人员", "MS－财务人员"),
                            ("临时额度管理", "临时额度管理"),
                            (" 临时额度管理", " 临时额度管理"),
                            ("MS系统管理员", "MS系统管理员"),
                            ("催收-账单", "催收-账单"),
                            ("售后退款", "售后退款"),
                            ("商品利率管理员", "商品利率管理员"),
                            ("电核", "电核"),
                            ("MS-电核", "MS-电核"),
                            ("MS-活动审批", "MS-活动审批"),
                            ("新版首页", "新版首页"),
                            ("MS-采购单推单配置", "MS-采购单推单配置"),
                            ("MS-采购单推单配置审核", "MS-采购单推单配置审核"),
                            ("MS - 采购单自动推单配置（慎重添加）", "MS - 采购单自动推单配置（慎重添加）"),
                            ("MS - 模型管理", "MS - 模型管理"),
                            ("优惠券管理", "优惠券管理"),
                            ("专题页管理", "专题页管理"),
                            ("MS-运营平台", "MS-运营平台"),
                            ("采购单管理", "采购单管理"),
                            ("订单管理", "订单管理"),
                            ("订单挂起释放关单", "订单挂起释放关单"),
                            ("来分期分类页配置", "来分期分类页配置"),
                            ("趣店分类页配置", "趣店分类页配置"),
                            ("修改姓名和身份证", "修改姓名和身份证"),
                            ("移动端管理员", "移动端管理员"),
                            ("类目管理", "类目管理"),
                            ("用户负面白名单", "用户负面白名单"),
                            ("MS管理员", "MS管理员"),
                            ("MS商品管理", "MS商品管理"),
                            ("MS商家管理", "MS商家管理"),
                            ("MS-招商-开放平台", "MS-招商-开放平台"),
                            ("开放平台", "开放平台"),
                            ("查看订单合同", "查看订单合同"),
                            ("订单日志", "订单日志"),
                            ("来分期H5页面配置", "来分期H5页面配置"),
                            ("商务系统权限", "商务系统权限"),
                            ("商品利率管理权限", "商品利率管理权限"),
                            ("商品运营权限", "商品运营权限"),
                            ("催收取消订单", "催收取消订单"),
                            ("客服取消订单", "客服取消订单"),
                            ("商品列表", "商品列表"),
                            ("商品评分管理", "商品评分管理"),
                            ("催收电核", "催收电核"),
                            ("拉灰解灰用户", "拉灰解灰用户"),
                            ("用户管理", "用户管理"),
                            ("开屏广告位配置", "开屏广告位配置"),
                            ("商品运营权限-商品报价审核", "商品运营权限-商品报价审核"),
                            ("商品运营权限-商品管理-查看报价", "商品运营权限-商品管理-查看报价"),
                            ("品牌管理", "品牌管理"),
                            ("个人中心轮播图", "个人中心轮播图"),
                            ("MS新品审核", "MS新品审核"),
                            ("MS报价自动审核规则", "MS报价自动审核规则"),
                            ("来分期运营配置新版首页", "来分期运营配置新版首页"),
                            ("批量关联供应商", "批量关联供应商"),
                            ("品牌绑定前端类目", "品牌绑定前端类目"),
                            ("采销leader-报价自动审核确认", "采销leader-报价自动审核确认"),
                            ("敏感信息不可查看", "敏感信息不可查看"),
                            ("支付明细", "支付明细"),
                            ("新客服权限", "新客服权限"),
                            ("新售后模块", "新售后模块"),
                            ("新模型管理", "新模型管理"),
                            ("新订单挂起释放关单", "新订单挂起释放关单"),
                            ("新用户负面名单", "新用户负面名单"),
                            ("新支付明细", "新支付明细"),
                            ("新商品运营权限-商品管理-查看报价", "新商品运营权限-商品管理-查看报价"),
                            ("新开发", "新开发"),
                            ("类目管理-leader", "类目管理-leader"),
                            ("采销leader权限", "采销leader权限"),
                            ("推荐广告位配置", "推荐广告位配置"),
                            ("商务系统权限-leader", "商务系统权限-leader"),
                            ("来分期运营配置", "来分期运营配置"),
                            ("解除代扣芝麻修改手机号", "解除代扣芝麻修改手机号"),
                            ("修改用户信息", "修改用户信息"),
                            ("解除支付宝绑定", "解除支付宝绑定"),
                            ("订单管理-无敏感信息", "订单管理-无敏感信息"),
                            ("催收账单-无敏感信息", "催收账单-无敏感信息"),
                            ("BI审核", "BI审核"),
                            ("活动管理审核", "活动管理审核")]}),

)

oo_mis = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("人力资源", "人力资源"),
                            ("商品运营", "商品运营"),
                            ("客服", "客服"),
                            ("线下运营", "线下运营"),
                            ("线下商户类目管理 ", "线下商户类目管理 "),
                            ("地方短信查询", "地方短信查询"),
                            ("审核组", "审核组"),
                            ("商户客服", "商户客服"),
                            ("人员管理", "人员管理"),
                            ("订单管理", "订单管理"),
                            ("角色管理", "角色管理"),
                            ("开发人员", "开发人员"),
                            ("运营管理", "运营管理"),
                            ("商品管理", "商品管理"),
                            ("商品类目属性管理", "商品类目属性管理"),
                            ("国政通运营学校", "国政通运营学校"),
                            ("趣券运营", "趣券运营"),
                            ("广告投放", "广告投放"),
                            ("采购单管理", "采购单管理"),
                            ("趣租运营", "趣租运营"),
                            ("用户查看", "用户查看"),
                            ("电核组", "电核组"),
                            ("催收组", "催收组"),
                            ("审核待分配", "审核待分配"),
                            ("供应商管理", "供应商管理"),
                            ("活动配置", "活动配置"),
                            ("专题管理", "专题管理"),
                            ("联盟费用提现", "联盟费用提现"),
                            ("兼职费用提现", "兼职费用提现"),
                            ("商户费用提现", "商户费用提现"),
                            ("租房费用提现", "租房费用提现"),
                            ("租房费用审核", "租房费用审核"),
                            ("兼职费用审核", "兼职费用审核"),
                            ("联盟费用审核", "联盟费用审核"),
                            ("趣支付退款", "趣支付退款"),
                            ("商户结算 广告配置", "商户结算 广告配置"),
                            ("账单管理", "账单管理"),
                            ("用户信息修改", "用户信息修改"),
                            ("趣租申请列表", "趣租申请列表"),
                            ("趣租账单管理", "趣租账单管理"),
                            ("趣租客服", "趣租客服"),
                            ("趣券退款", "趣券退款"),
                            ("芝麻信息查询", "芝麻信息查询"),
                            ("趣租审核", "趣租审核"),
                            ("趣租配置", "趣租配置"),
                            ("趣租订单修改", "趣租订单修改"),
                            ("财务报表 趣租代付", "财务报表 趣租代付"),
                            ("银行管理", "银行管理"),
                            ("联盟费用结算", "联盟费用结算"),
                            ("趣租退租管理", "趣租退租管理"),
                            ("供应商结算", "供应商结算"),
                            ("趣租账单修改", "趣租账单修改"),
                            ("联盟财务审核", "联盟财务审核"),
                            ("供应商报价管理", "供应商报价管理"),
                            ("签单费提现", "签单费提现"),
                            ("趣点抢购维护", "趣点抢购维护"),
                            ("用户申诉审核", "用户申诉审核"),
                            ("高亮规则管理", "高亮规则管理"),
                            ("趣店公告管理", "趣店公告管理"),
                            ("广告效果查看", "广告效果查看"),
                            ("趣店管理", "趣店管理"),
                            ("抽奖明细", "抽奖明细"),
                            ("失联修复", "失联修复"),
                            ("优惠券管理 首页配置", "优惠券管理 首页配置"),
                            ("期待乐管理", "期待乐管理"),
                            ("实习生管理", "实习生管理"),
                            ("详细照片", "详细照片"),
                            ("充值查询", "充值查询"),
                            ("微信数据查看", "微信数据查看"),
                            ("编辑联系方式", "编辑联系方式"),
                            ("offer审核", "offer审核"),
                            ("offer电核", "offer电核"),
                            ("V1+审核 商品评分", "V1+审核 商品评分"),
                            ("催收分配", "催收分配"),
                            ("无密支付开关", "无密支付开关"),
                            ("用户激活审核", "用户激活审核"),
                            ("无学籍审核", "无学籍审核"),
                            ("劳务税管理", "劳务税管理"),
                            ("数据统计", "数据统计"),
                            ("线下商户结算 线下商户提现", "线下商户结算 线下商户提现"),
                            ("app tab 配置", "app tab 配置"),
                            ("取消工单", "取消工单"),
                            ("微信菜单管理", "微信菜单管理"),
                            ("人脸授信电核", "人脸授信电核"),
                            ("秒杀配置 转化率统计", "秒杀配置 转化率统计"),
                            ("小贷公司配置", "小贷公司配置"),
                            ("数据监控", "数据监控"),
                            ("sku关联配置", "sku关联配置"),
                            ("热搜词管理", "热搜词管理"),
                            ("自动推单", "自动推单"),
                            ("负面白名单管理", "负面白名单管理"),
                            ("电催管理员", "电催管理员"),
                            ("催收组长", "催收组长"),
                            ("线下商品管理", "线下商品管理"),
                            ("新趣租后台", "新趣租后台"),
                            ("mis运营管理", "mis运营管理"),
                            ("运营管理全", "运营管理全"),
                            ("自动推单-价格审批", "自动推单-价格审批"),
                            ("商品管理全", "商品管理全"),
                            ("品牌管理", "品牌管理"),
                            ("测试人员工具", "测试人员工具")]}),

)

oo_laifenqi = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("总管", "总管"),
                            ("客服", "客服"),
                            ("开发", "开发"),
                            ("测试", "测试"),
                            ("运营", "运营"),
                            ("售后", "售后"),
                            ("客服管理", "客服管理"),
                            ("催收", "催收"),
                            ("电销电核", "电销电核"),
                            ("采购", "采购"),
                            ("风控", "风控"),
                            ("财务专员 财务管理员", "财务专员 财务管理员"),
                            ("催收管理员", "催收管理员"),
                            ("财务数据分析", "财务数据分析"),
                            ("QD项目", "QD项目"),
                            ("账单处理专员", "账单处理专员"),
                            ("趣租总管", "趣租总管"),
                            ("电销导入", "电销导入"),
                            ("售后管理员", "售后管理员"),
                            ("报表统计", "报表统计"),
                            ("客服头子", "客服头子"),
                            ("客服-取消代扣 客服-异常还款", "客服-取消代扣 客服-异常还款"),
                            ("商品管理", "商品管理"),
                            ("趣租审核", "趣租审核"),
                            ("趣租催收", "趣租催收"),
                            ("趣租审核专员", "趣租审核专员"),
                            ("供应商管理", "供应商管理"),
                            ("客服-恢复额度 商品分期运营", "客服-恢复额度 商品分期运营"),
                            ("趣店－售后", "趣店－售后"),
                            ("趣店采购", "趣店采购"),
                            ("来分期－运营主管", "来分期－运营主管"),
                            ("来分期－电销主管 来分期－数据运营主管", "来分期－电销主管 来分期－数据运营主管"),
                            ("来分期－数据主管", "来分期－数据主管"),
                            ("来分期－app运营主管", "来分期－app运营主管"),
                            ("来分期－风控主管", "来分期－风控主管"),
                            ("趣店－客服", "趣店－客服"),
                            ("技术－总管 后台主管", "技术－总管 后台主管"),
                            ("客服－取消订单权限", "客服－取消订单权限"),
                            ("趣租－管理员", "趣租－管理员"),
                            ("新趣租-审核", "新趣租-审核"),
                            ("测试人员", "测试人员"),
                            ("查看订单日志", "查看订单日志"),
                            ("催收－白名单管理 马上退款", "催收－白名单管理 马上退款"),
                            ("手工批量退款", "手工批量退款"),
                            ("账单减免权限", "账单减免权限"),
                            ("财务退款", "财务退款"),
                            ("作废订账单", "作废订账单"),
                            ("电核专员", "电核专员"),
                            ("芝麻数据反馈 测试任意人员账号", "芝麻数据反馈 测试任意人员账号"),
                            ("取消和作废订单", "取消和作废订单"),
                            ("电核员", "电核员"),
                            ("查看合同", "查看合同"),
                            ("电核管理员", "电核管理员"),
                            ("财务结算", "财务结算"),
                            ("冻结用户", "冻结用户"),
                            ("订账单查看 电销查看订单列表", "订账单查看 电销查看订单列表"),
                            ("授权解冻", "授权解冻"),
                            ("线下账单信息修改", "线下账单信息修改"),
                            ("平台降级策略", "平台降级策略"),
                            ("重发打款", "重发打款"),
                            ("消息管理", "消息管理"),
                            ("消息推送 来分期－消息推送", "消息推送 来分期－消息推送"),
                            ("财务-财务结算", "财务-财务结算"),
                            ("查看权限", "查看权限"),
                            ("订单流转", "订单流转"),
                            ("首页配置", "首页配置"),
                            ("运营-首页配置", "运营-首页配置"),
                            ("汽车-审核组 优惠券管理", "汽车-审核组 优惠券管理"),
                            ("消息管理权限", "消息管理权限"),
                            ("查看账单日志", "查看账单日志"),
                            ("订单挂起", "订单挂起"),
                            ("活动配置", "活动配置"),
                            ("优惠券临时额度管理", "优惠券临时额度管理"),
                            ("催收-账单手工代扣", "催收-账单手工代扣"),
                            ("订单列表操作日志查看", "订单列表操作日志查看"),
                            ("APP管理", "APP管理"),
                            ("操作订单日志", "操作订单日志"),
                            ("挂起订单管理", "挂起订单管理"),
                            ("订单管理", "订单管理"),
                            ("账单管理", "账单管理"),
                            ("测试人员工具 电核员2", "测试人员工具 电核员2"),
                            ("催收取消订单", "催收取消订单"),
                            ("售后1", "售后1"),
                            ("采购单管理", "采购单管理"),
                            ("用户拉灰解灰", "用户拉灰解灰"),
                            ("账单减免", "账单减免"),
                            ("客服取消订单", "客服取消订单"),
                            ("日志 操作日志查看", "日志 操作日志查看"),
                            ("查看用户手机号", "查看用户手机号"),
                            ("查看地址", "查看地址"),
                            ("取消保险单", "取消保险单"),
                            ("用户电话修改", "用户电话修改"),
                            ("用户标签管理", "用户标签管理"),
                            ("批量导出订单合同", "批量导出订单合同"),
                            ("调研问卷管理", "调研问卷管理"),
                            ("临时额度管理", "临时额度管理")]}),

)


oo_datahouse = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("开发人员", "开发人员"),
                            ("财务组", "财务组"),
                            ("金融合作", "金融合作"),
                            ("财务组root", "财务组root"),
                            ("财务组（学生&p2p应还，未来应收）", "财务组（学生&p2p应还，未来应收）"),
                            ("财务组（订单明细）", "财务组（订单明细）"),
                            ("财务组(实收还款)", "财务组(实收还款)"),
                            ("财务组(实收还款明细)", "财务组(实收还款明细)"),
                            ("财务组（自然月逾期明细）", "财务组（自然月逾期明细）"),
                            ("产品组", "产品组"),
                            ("root", "root"),
                            ("p2p只读", "p2p只读"),
                            ("导出脚本文件", "导出脚本文件"),
                            ("财务组-来分期应收明细", "财务组-来分期应收明细"),
                            ("分润系统(报表)", "分润系统(报表)"),
                            ("测试人员", "测试人员"),
                            ("孙海莹", "孙海莹"),
                            ("产品组（报表）", "产品组（报表）"),
                            ("分润系统（小贷公司日报）", "分润系统（小贷公司日报）"),
                            ("趣钱包订单明细", "趣钱包订单明细"),
                            ("财务组-来分期白条，实物订单明细", "财务组-来分期白条，实物订单明细"),
                            ("小贷监管报表", "小贷监管报表"),
                            ("未来百日应收", "未来百日应收"),
                            ("线下商户汇总", "线下商户汇总"),
                            ("小贷报表（应收放款汇总）", "小贷报表（应收放款汇总）"),
                            ("小贷报表（逾期明细）", "小贷报表（逾期明细）"),
                            ("分润系统（应付汇总）", "分润系统（应付汇总）"),
                            ("要借钱明细", "要借钱明细"),
                            ("零钱代扣明细", "零钱代扣明细"),
                            ("来分期小贷权限", "来分期小贷权限"),
                            ("金融办--分润", "金融办--分润"),
                            ("商城代扣收款明细", "商城代扣收款明细"),
                            ("信托系统", "信托系统"),
                            ("马上金融报表", "马上金融报表"),
                            ("来分期-金融合作", "来分期-金融合作"),
                            ("Datahouse系统管理员", "Datahouse系统管理员"),
                            ("渤海信托", "渤海信托"),
                            ("马上金融-逾期结算报表", "马上金融-逾期结算报表"),
                            ("ipo逾期", "ipo逾期"),
                            ("datahouse汇总日报", "datahouse汇总日报"),
                            ("马上金融－收款明细", "马上金融－收款明细"),
                            ("借呗明细", "借呗明细"),
                            ("资金组", "资金组")]}),
)


oo_callcenter = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("用户申诉审核", "用户申诉审核"),
                            ("呼叫中心-质检员", "呼叫中心-质检员"),
                            ("呼叫中心-管理", "呼叫中心-管理"),
                            ("呼叫中心-普通用户", "呼叫中心-普通用户")]}),
)

oo_marketing = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("定时任务审批", "定时任务审批"),
                            ("创建定时任务", "创建定时任务"),
                            ("任务效果", "任务效果"),
                            ("业务审批人", "业务审批人"),
                            ("营销中心后台-提额任务清单", "营销中心后台-提额任务清单"),
                            ("营销中心后台-风控审批", "营销中心后台-风控审批"),
                            ("营销中心后台-创建提额", "营销中心后台-创建提额"),
                            ("营销中心管理员", "营销中心管理员"),
                            ("营销中心后台-运营", "营销中心后台-运营"),
                            ("营销活动管理员", "营销活动管理员"),
                            ("营销活动管理-定时任务审批", "营销活动管理-定时任务审批"),
                            ("营销活动管理-活动列表", "营销活动管理-活动列表")]}),
)

oo_debt = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("电核人员", "电核人员"),
                            ("核销专员", "核销专员"),
                            ("前端主管", "前端主管"),
                            ("催收系统-品控", "催收系统-品控"),
                            ("催收系统-客服对接", "催收系统-客服对接"),
                            ("综合支持", "综合支持"),
                            ("外呼管理岗", "外呼管理岗"),
                            ("运营主管", "运营主管"),
                            ("部门负责人", "部门负责人"),
                            ("小旋风", "小旋风"),
                            ("运营", "运营"),
                            ("后端组长/主管", "后端组长/主管"),
                            ("前/中端组长", "前/中端组长"),
                            ("前/中/后端组员", "前/中/后端组员"),
                            ("催收系统-开发测试", "催收系统-开发测试")]}),
)

oo_risk = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("风控权限分配", "风控权限分配"),
                            ("风控后台", "风控后台")]}),
)

oo_payadmin = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("支付管理后台－渠道管理员", "支付管理后台－渠道管理员"),
                            ("支付管理后台-结算管理员", "支付管理后台-结算管理员"),
                            ("支付后台管理-结算业务操作员", "支付后台管理-结算业务操作员"),
                            ("支付管理后台-对账管理员", "支付管理后台-对账管理员"),
                            ("支付管理后台-对账操作员", "支付管理后台-对账操作员"),
                            ("支付管理后台-对账结果管理", "支付管理后台-对账结果管理"),
                            ("支付渠道查看", "支付渠道查看"),
                            ("趣分期结算系统-打款明细", "趣分期结算系统-打款明细"),
                            ("资金预测管理员", "资金预测管理员"),
                            ("资金预测领导", "资金预测领导"),
                            ("资金预测财务人员", "资金预测财务人员"),
                            ("p2p推标平台管理员", "p2p推标平台管理员"),
                            ("p2p推标平台一期管理员", "p2p推标平台一期管理员"),
                            ("分润管理员", "分润管理员"),
                            ("分润操作员", "分润操作员"),
                            ("资金预测运营人员", "资金预测运营人员"),
                            ("p2p推标平台报表汇总", "p2p推标平台报表汇总"),
                            ("p2p推标平台赎回操作", "p2p推标平台赎回操作"),
                            ("支付交易管理员", "支付交易管理员"),
                            ("支付交易订单查看", "支付交易订单查看"),
                            ("清分管理员", "清分管理员"),
                            ("支付网关管理员", "支付网关管理员"),
                            ("清分债转操作员", "清分债转操作员"),
                            ("渠道-代付支付单信息查询", "渠道-代付支付单信息查询"),
                            ("结算单打款明细", "结算单打款明细"),
                            ("交易运营平台", "交易运营平台"),
                            ("投保系统平台管理员", "投保系统平台管理员"),
                            ("分润产品操作", "分润产品操作"),
                            ("支付结转单信息查询", "支付结转单信息查询"),
                            ("计费管理员", "计费管理员"),
                            ("保险管理平台", "保险管理平台"),
                            ("渠道-代扣支付信息查询", "渠道-代扣支付信息查询"),
                            ("渠道-代付批次信息查询", "渠道-代付批次信息查询")]}),
)

oo_financeadmin = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("金融组－研发", "金融组－研发"),
                            ("金融组－p2p－报表", "金融组－p2p－报表"),
                            ("金融组－p2p－推标", "金融组－p2p－推标"),
                            ("金融组－p2p－赎回操作", "金融组－p2p－赎回操作"),
                            ("金融组－applo－文件上传", "金融组－applo－文件上传"),
                            ("金融组－applo－报表", "金融组－applo－报表"),
                            ("金融组－abs－小贷第三方", "金融组－abs－小贷第三方"),
                            ("金融组－abs－保理第三方", "金融组－abs－保理第三方"),
                            ("金融组－abs－后台管理", "金融组－abs－后台管理"),
                            ("金融组－applo－对账", "金融组－applo－对账"),
                            ("ares-分润报表", "ares-分润报表"),
                            ("项目部署", "项目部署"),
                            ("SFTP_CONFIG", "SFTP_CONFIG"),
                            ("金融组－apple－补单", "金融组－apple－补单"),
                            ("资金管理后台-还款计划", "资金管理后台-还款计划"),
                            ("渤海信托01", "渤海信托01"),
                            ("ABS-专项计划列表", "ABS-专项计划列表"),
                            ("ares-融资成本", "ares-融资成本"),
                            ("厦门信托", "厦门信托")]}),
)

oo_bitools = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("HiveSQL提数", "HiveSQL提数")]}),
)

oo_biadmin = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("链接配置", "链接配置"),
                            ("bi_admin开发", "bi_admin开发")]}),
)

oo_monitor = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("监控中心—反作弊监控查看", "监控中心—反作弊监控查看"),
                            ("监控中心—反作弊监控管理", "监控中心—反作弊监控管理"),
                            ("监控中心—趣店监控管理", "监控中心—趣店监控管理"),
                            ("监控中心—趣店监控查看", "监控中心—趣店监控查看"),
                            ("监控中心—来分期监控管理", "监控中心—来分期监控管理"),
                            ("监控中心—来分期监控查看", "监控中心—来分期监控查看"),
                            ("监控中心—趣钱包监控管理", "监控中心—趣钱包监控管理"),
                            ("监控中心—趣钱包监控查看", "监控中心—趣钱包监控查看"),
                            ("监控中心—渠道监控管理", "监控中心—渠道监控管理"),
                            ("监控中心—渠道监控查看", "监控中心—渠道监控查看"),
                            ("监控中心—要借钱监控查看", "监控中心—要借钱监控查看"),
                            ("监控中心—要借钱监控管理", "监控中心—要借钱监控管理"),
                            ("监控中心—风控监控管理", "监控中心—风控监控管理"),
                            ("监控中心—风控监控查看", "监控中心—风控监控查看"),
                            ("监控中心-活动配置员", "监控中心-活动配置员"),
                            ("监控中心-数据查看-all", "监控中心-数据查看-all"),
                            ("监控中心-dashboard排序管理员", "监控中心-dashboard排序管理员"),
                            ("监控中心-数据脱敏校验", "监控中心-数据脱敏校验"),
                            ("监控中心-审核管理", "监控中心-审核管理"),
                            ("春眠监控管理员", "春眠监控管理员"),
                            ("趣先享监控查看", "趣先享监控查看"),
                            ("趣先享监控管理", "趣先享监控管理"),
                            ("trace查看", "trace查看"),
                            ("监控中心-Trace-super管理员", "监控中心-Trace-super管理员"),
                            ("监控中心-灰度发布管理员", "监控中心-灰度发布管理员"),
                            ("监控中心-灰度发布-qa-配置员", "监控中心-灰度发布-qa-配置员"),
                            ("监控中心-灰度发布-op-配置员", "监控中心-灰度发布-op-配置员"),
                            ("监控中心-反欺诈-管理员", "监控中心-反欺诈-管理员"),
                            ("监控中心-来分期延迟库备用管理员", "监控中心-来分期延迟库备用管理员"),
                            ("监控中心-来分期性能日报", "监控中心-来分期性能日报")]}),
)

oo_grafana = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("趣店监控", "趣店监控"), ("来分期监控", "来分期监控"), ("后台", "后台"), ("风控", "风控"), ("系统性能", "系统性能")]}),
)

oo_qc = (
    Inputs(name="applyrole", title="申请角色", inputtype="multiselect", desc="",
           style={"div-class": "span12", "input-class": 'input-normal',
                  'items': [("质检中心-客服", "质检中心-客服"), ("质检中心-质检", "质检中心-质检"), ("质检中心-管理", "质检中心-管理")]}),
)

dic_applylist = OrderedDict([("MS后台", oo_ms), ("MIS后台", oo_mis), ("来分期后台", oo_laifenqi), ("数据仓库", oo_datahouse), ("呼叫中心", oo_callcenter), ("营销中心", oo_marketing), ("催收系统", oo_debt), (
    "风控后台", oo_risk), ("支付管理后台", oo_payadmin), ("资金管理后台", oo_financeadmin), ("BI工具后台", oo_bitools), ("BI管理后台", oo_biadmin), ("监控后台", oo_monitor), ("Grafana", oo_grafana), ("质检中心", oo_qc)])


def menu_list_get(username):
    return """[{
            id:'redis',
            menu:[
             {
              text:'常用操作',
              items:[
                {id:'mysqlaccoutinfo',text:'权限申请',href:'mysqlaccoutinfo.html'},
                {id:'fuckadmin',text:'管理页面',href:'fuckadmin.html'}
              ]
            }
       
              ]
          }

          ]"""


def login_mail(request):
    dic_html = {}
    mana_login = pub_def.mana_login()
    login_result, login_mess = False, ""
    if request.method == 'POST':
        username = replace_chart(request.POST['username'])
        login_result, login_mess = mana_login.login_mail(username)
        if "请点击邮件里的链接完成登录" in login_mess:
            login_mess = ''' <div class="tips tips-large tips-success">
          <span class="x-icon x-icon-success"><i class="icon icon-ok icon-white"></i></span>
          <div class="tips-content">
            <h2>提交成功</h2>
            <p class="auxiliary-text">
              %s
            </p>
          </div></div>''' % login_mess
        else:
            login_mess = ''' <div class="tips tips-large tips-warning">
          <span class="x-icon x-icon-error"><i class="icon icon-ok icon-white"></i></span>
          <div class="tips-content">
            <h2>提交成功</h2>
            <p class="auxiliary-text">
              %s
            </p>
          </div></div>''' % login_mess
        # if login_result:
        #    response = HttpResponseRedirect("/")
    else:
        action = request.GET.get('action', '')
        username = replace_chart(request.GET.get('username', ''))
        if action == "reg":
            newkey = request.GET.get('newkey', '')
            login_result, login_mess = mana_login.login_reg(username, newkey)
        elif action == "del":
            response = HttpResponseRedirect('/login.html')
            response.delete_cookie("token")
            response.delete_cookie('chs')
            return response
    if login_result:
        response = HttpResponseRedirect('/main.html')
        mana_login.login_ok(request, response, username)
        return response
    else:
        dic_html["mess"] = login_mess
        dic_html["username"] = request.COOKIES.get("username", "")
    return render(request, 'loginmail.html', dic_html)


@login_required
def main_html(request):
    dic_html = {}
    dic_html["username"] = request.COOKIES.get("username", "****")
    dic_html["menustr"] = menu_list_get("")
    return render(request, 'main.html', dic_html)


@login_required
def apply_list(request):
    mana_login = pub_def.mana_login()
    res_flag, res_num, res_info = mana_login.checkuserToken(request, 1)
    if res_flag == False:
        redirect('/login.html')
    headstr = """<div style="margin-bottom:5px;"><a href="mysqlaccoutinfo_add.html?action=new" class="button button-small"><i class="icon-plus"></i>新权限申请</a></div>"""
    htmlstr_list, js_file_list, css_file_list, html_footer_list = apply_list_html(
        request)
    dic_html = {}
    js_file = js_file_list
    #addr_to = list(set(js_file))
    # addr_to.sort(key=js_file.index)
    dic_html["title"] = "申请列表"
    dic_html["jsfile"] = "\n".join(js_file)
    dic_html["cssfile"] = ""
    dic_html["htmlstr"] = '%s\n<div style="width:1300px">%s</div>' % (
        headstr, htmlstr_list)
    dic_html["script_footer"] = html_footer_list
    return render(request, 'view_base.html', dic_html)


def getResultSQL(sqlstr, isautoclose=True, maxrows=9999):
    connection = MySQLdb.connect(
        host='localhost', port=3306, user='root', passwd='hehe', db='djangoDB')
    connection.set_character_set('utf8')
    cursor = connection.cursor()
    step_starttime = time.time()
    cursor.execute(sqlstr)
    #rows = cursor.fetchall()
    rows = cursor.fetchmany(maxrows)
    columns = [t[0] for t in cursor.description]
    cursor.close()
    # if isautoclose:
    #    connection.close()
    select_times = {'runtimes': int((time.time() - step_starttime) * 1000)}
    connection.close()
    return rows, columns, select_times


def getResultSQL_para(sqlstr, para, maxrows=9999):
    connection = MySQLdb.connect(
        host='localhost', port=3306, user='root', passwd='hehe', db='djangoDB')
    connection.set_character_set('utf8')
    cursor = connection.cursor()
    step_starttime = time.time()
    cursor.execute(sqlstr, para)
    #rows = cursor.fetchall()
    rows = cursor.fetchmany(maxrows)
    columns = [t[0] for t in cursor.description]
    cursor.close()
    # connection.close()
    select_times = {'runtimes': int((time.time() - step_starttime) * 1000)}
    connection.close()
    return rows, columns, select_times


def apply_list_html(request):
    userinfo = mana_login().get_userinfo(request)
    username = userinfo.get("username", "")
    #username = replace_chart(request.GET.get('username', ''))
    sqlstr = """select id,applyuser,applyname,applytype,applymobile,applyrole,case when applystatus=1 then '新申请'
when applystatus=2 then '<span class="label label-info">已审批</span>'
when applystatus=-2 then '<span class="label label-warning">已拒绝</span>'
when applystatus=9 then '<span class="label label-success">流程成功</span>'
when applystatus=-9 then '<span class="label label-important">流程失败</span>' end as applystatus
,applytime,approver,approvetime,secuser,dotime,concat('<a href="mysqlaccoutinfo_add.html?id=',id,'">详细</a>') as editurl from apply_list where applyuser=%s order by id desc"""
    rows, columns, select_times = getResultSQL_para(sqlstr, (username,))
    grid_format = {}
    grid_format["columns"] = '''
            {title : 'id',dataIndex :'id', width:40}
            ,{title : '申请人',dataIndex :'applyuser', width:100}
            ,{title : '姓名',dataIndex :'applyname', width:100}
            ,{title : '手机号',dataIndex :'applymobile', width:100}
            ,{title : '申请后台',dataIndex :'applytype', width:120}
            ,{title : '当前状态',dataIndex :'applystatus', width:100}
            ,{title : '申请权限',dataIndex : 'applyrole',width:240,renderer: Format.cutTextRenderer(30)}
            ,{title : '申请时间',dataIndex :'applytime', width:130}
            ,{title : '审批人',dataIndex :'approver', width:100}
            ,{title : '审批时间',dataIndex :'approvetime', width:130}
            ,{title : '处理人',dataIndex :'secuser', width:100}
            ,{title : '完成时间',dataIndex :'dotime', width:130}
            ,{title : '操作',dataIndex : 'editurl',elCls : 'center',width:50}
           '''
    grid_format["grid_style"] = """,bbar:{pagingBar:true}"""
    grid_format["store_style"] = """,pageSize:20"""
    #htmlstr, js_file, css_file, html_footer=apply_list()
    return fmt_html.bui.make_static_grid(rows, columns, 0, grid_format)


def exe_sql_para_format(sqlstr, paras, formatstr=""):
    # print("*****>sql_.py")
    connection = MySQLdb.connect(
        host='localhost', port=3306, user='root', passwd='hehe', db='djangoDB')
    connection.set_character_set('utf8')
    dic_return = {'formatstr': formatstr}
    cursor = connection.cursor()
    step_starttime = time.time()
    cursor.execute(sqlstr, paras)
    if("insertid" in formatstr):
        # print("*****>")
        dic_return['insertid'] = connection.insert_id()

    connection.commit()
    cursor.close()
    dic_return['runtimes'] = int((time.time() - step_starttime) * 1000)
    connection.close()
    # print("*****>sql_.py")
    # print(dic_return)
    return True, dic_return


@login_required
def apply_form(request):
    userinfo = mana_login().get_userinfo(request)
    session_username = userinfo.get("username", "")
    applymobile = request.POST.get("applymobile", "")
    applyname = request.POST.get("applyname", "")

    approver = ""
    apply_step = 0
    applyid = 0
    sb_html = []
    action = request.GET.get("action", "add")
    applytype = request.GET.get("mtype", "MS后台")
    if request.method == 'GET':
        applyid = int(request.GET.get("id", "0"))
    else:
        applyid = int(request.POST.get("applyid"))  # pass #用户提交
        applystatus = int(request.POST.get("applystatus"))
        if applystatus == 0:
            applytype = request.POST.get("applytype")
            username = session_username
            applyvalue1_list = []
            inputlist = dic_applylist.get(applytype, [])
            for input_tmp in inputlist:
                print input_tmp
                namestr = input_tmp.name
                print namestr
                titlestr = input_tmp.title
                print titlestr
                applyvalue1_list.append((titlestr, request.POST.get(namestr)))
                print applyvalue1_list
            applyvalue = simplejson.dumps(applyvalue1_list)
            print applyvalue
            #applyvalue2 = request.POST.get("applyvalue2")
            #applyvalue3 = request.POST.get("applyvalue3")

            applyrole = request.POST.get("applyrole")
            approver = request.POST.get("approver")
            applyreason = request.POST.get("applyreason")
            applytoken = get_random_str(20)
            sectoken = get_random_str(15)
            if applymobile == "":
                sb_html.append(fmt_html.bui.make_smalltips(
                    "手机号不能为空", "warning"))
            elif approver == "":
                sb_html.append(fmt_html.bui.make_smalltips(
                    "审批人不能为空", "warning"))
            elif applyname == "":
                sb_html.append(
                    fmt_html.bui.make_smalltips("姓名不能为空", "warning"))
            else:
                sqlstr = "insert into apply_list(applystatus,applyuser,applyname,applytype,applymobile,applyrole,applyreason,applytime,approver,applytoken,sectoken) values(1,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s)"
                # sb_html.append("<div>%s,%s,%s,%s,%s,%s</div>"%(applyid,applystatus,username,dbname,dbowner,applyreson))
                paras = (username, applyname, applytype, applymobile,
                         applyrole, applyreason, approver, applytoken, sectoken)
                exec_result, dic_result = exe_sql_para_format(
                    sqlstr, paras, "insertid")
                print dic_result
                if exec_result:
                    applyid = int(dic_result.get("insertid", 0))
                    print applyid
                    if applyid > 0:
                        #changetokenstr_ok = "%s|%s|%s|%s|%s" % (applyid, 1, 2, ownertoken, dbowner)
                        #changetokenstr_err = "%s|%s|%s|%s|%s" % (applyid, 1, -2, ownertoken, dbowner)
                        apply_token_makesend(applyid, 1)
                        sb_html.append(fmt_html.bui.make_smalltips(
                            "提交申请成功！", "seccess"))
                        HttpResponseRedirect("mysqlaccoutinfo.html")
                    else:
                        sb_html.append(fmt_html.bui.make_smalltips(
                            "提交申请没有返回正确的id！", "warning"))
                else:
                    sb_html.append(fmt_html.bui.make_smalltips(
                        "提交申请失败！", "warning"))
        elif applystatus in (1, 2):
            hid_button_value = request.POST.get("hid_button")
            #{"btnok":1,"btnno":-1,"btncancle":0}.get(hid_button_value,)
            if hid_button_value == "btnok":
                newapplystatus = applystatus + 1
            elif hid_button_value == "btnno" and applystatus > 0:
                newapplystatus = -(applystatus + 1)
            elif hid_button_value == "btncancle":
                newapplystatus = -1
            else:
                newapplystatus = 0
            change_result = changestatus(
                applyid, applystatus, newapplystatus, userinfo)
            if change_result:
                # newurl="mysqlaccoutinfo.html?applyid=%s"%(applyid,)
                HttpResponseRedirect("mysqlaccoutinfo.html?id=%s" % (applyid,))
        else:
            sb_html.append(applystatus)
    form_ = fmt_html.form_.form_()

    sb_html.append(form_.make_form_head(0, "Post", "?action=%s" % (action,)))
    applyid = int(applyid)
    if applyid == 0:
        apply_form_add(sb_html, form_, session_username, applyname,
                       applymobile, approver, applytype, apply_step)
    else:
        apply_form_display(sb_html, form_, applyid, userinfo)
        # redirect('/mysqlaccoutinfo.html')

    #htmlstr_list, js_file_list, css_file_list, html_footer_list = apply_list(request)
    dic_html = {}
    js_file = []
    # if len(js_file_list)>0:
    #    js_file.extend(js_file_list)
    if len(form_.Js_header):
        js_file.extend(form_.Js_header)

    #addr_to = list(set(js_file))
    # addr_to.sort(key=js_file.index)
    dic_html["title"] = "申请个人权限"
    dic_html["jsfile"] = "\n".join(js_file)
    dic_html["cssfile"] = ""
    dic_html["htmlstr"] = "\n".join(sb_html)
    dic_html["script_footer"] = fmt_html.bui.html_tips_title
    return render(request, 'forms.html', dic_html)


def apply_form_add(sb_html, form_, username, applyname, applymobile, approver, applytype, applyid):
    rowlist = []
    for key in dic_applylist:
        rowlist.append((key, key))
    sb_html.append(form_.make_hidden("applyid", applyid))
    sb_html.append(form_.make_hidden("applystatus", 0))
    selectonchangestr = """location.href='?action=new&mtype='+ev.item.text;"""
    sb_html.append(form_.make_input("applyuser", "申请人", username, "span12",
                                    '{"text":"请输入申请用户名","iconCls":"icon icon-user"}', "input-normal", "", "@qudian.com"))
    sb_html.append(form_.make_input("applyname", "姓名", applyname,
                                    "span12", '{"text":"请输入姓名"}', "input-normal"))
    sb_html.append(form_.make_input("applymobile", "手机号",
                                    applymobile, "span12", '{"text":"请输入手机号"}', "input-normal"))
    sb_html.append(form_.make_select("applytype", "申请后台", applytype,
                                     "span12", "input-normal", selectonchangestr, rowlist, ""))
    input_tmplist = dic_applylist.get(applytype, ())
    for input_tmp in input_tmplist:
        # paraid,title="",defaultvalue="",spanclass="span8",datatip=""
        sb_html.append(input_tmp.toHtml("", False))
    # sb_html.append(form_.make_input("applyvalue1","数据库名称",applyvalue1,"span24",'{"text":"多个数据库逗号分隔"}',"input-normal"))#paraid,title="",defaultvalue="",spanclass="span8",datatip=""
    # paraid,title="",defaultvalue="",spanclass="span8",datatip=""
    sb_html.append(form_.make_input("approver", "上级审批人", approver, "span12",
                                    '{"text":"请输入审批人","iconCls":"icon icon-user"}', "input-normal", "", "@qudian.com"))
    # paraid,title="",defaultvalue="",spanclass="span8",datatip=""
    sb_html.append(form_.make_textarea("applyreason", "申请理由",
                                       "", "span12", '', "input-large", "", ""))
    sb_html.append(form_.make_form_foot(
        0, [{"btntype": "submit", "btnclass": "button-primary", "id": "btnsave", "title": "提交", "action": ""}]))


def apply_form_display(sb_html, form_, applyid, userinfo):
    print 'apply_form_display'
    session_username = userinfo.get("username", "")
    print session_username
    sqlstr = "select id,applystatus,applyuser,applyname,applymobile,applyrole,applyreason,applytime,approver,approvetime,secuser,dotime from apply_list where id=%s;"
    rows, columsn, localreslut = getResultSQL_para(sqlstr, (applyid,))
    print rows[0]
    if len(rows) != 1:
        sb_html.append("出错了，没有找到指定id的信息")
    applyid, applystatus, applyuser, applyname, applymobile, applyrole, applyreason, applytime, approver, approvetime, secuser, dotime = rows[
        0]
    if 1:
        dic_status = {1: "已提交", 2: "已审核",
                      9: "已开通", -2: "上级审批已拒绝", -9: "执行结果出错"}
        sb_html.append(form_.make_hidden("applyid", applyid))
        sb_html.append(form_.make_hidden("applystatus", applystatus))
        #sb_html.append(""" <h2>{title}</h2><hr><div class="row detail-row">""".format(title=applytype))
        sb_html.append(form_.make_lable("申请ID", 1))
        sb_html.append(form_.make_lable(
            "当前状态", dic_status.get(applystatus, "NA")))
        sb_html.append(form_.make_lable("申请内容", decode_applyvalue1(applyrole)))
        sb_html.append(form_.make_lable("申请人", applyuser))
        sb_html.append(form_.make_lable("姓名", decode_applyvalue1(applyname)))
        sb_html.append(form_.make_lable("手机号", applymobile))
        sb_html.append(form_.make_lable("申请时间", applytime))
        sb_html.append(form_.make_lable("申请原因", applyreason))
        if abs(applystatus) > 1:
            sb_html.append(form_.make_lable("审批人", approver))
            sb_html.append(form_.make_lable("审批时间", approvetime))
            #sb_html.append(form_.make_lable("审批原因", ownerreson))
        if abs(applystatus) > 2:
            sb_html.append(form_.make_lable("处理时间", dotime))
        #    if session_username in (applyuser) or int(userinfo.get("userpower",0))>100:
        #        sb_html.append(form_.make_lable("处理结果", doresult))
        #    else:
        #        sb_html.append(form_.make_lable("处理结果", "*"*20))

    sb_html.insert(0, fmt_html.bui.make_stepbar(
        ("申请资源", "leader审批", "执行结果", "流程结束"), applystatus))
    if applystatus in (1, 2):
        if (applystatus == 1 and session_username == approver) or (applystatus == 2 and int(userinfo.get("userpower", 0)) > 100):
            sb_html.append(form_.make_form_foot(0, [{"btntype": "button", "btnclass": "button-success", "id": "btnok", "title": "同意", "action": "onclick_action"}, {
                           "btntype": "button", "btnclass": "button-warning", "id": "btnno", "title": "拒绝", "action": "onclick_action"}]))

    else:
        sb_html.append(form_.make_form_foot(0, []))
    # sb_html.append(form_.make_form_script())


def decode_applyvalue1(applyvalue1):
    if '[' not in applyvalue1:
        return applyvalue1
    sb_applist = []
    # sb_applist.append("<ul>")

    jsonobject = simplejson.loads(applyvalue1, encoding="utf8")
    for title, value in jsonobject:
        sb_applist.append("<span><b>%s</b>:%s</span>&nbsp;" % (title, value))

    # sb_applist.append("</ul>")
    return "".join(sb_applist)


# def apply_list_html(request):
#    sqlstr="select id,applyuser,applyrole,applyvalue,applyreason,applytime,approver from apply_list;"
#   rows, columns, select_times =  getResultSQL(sqlstr)
#    grid_format={}
#    grid_format["columns"]='''
#            {title : 'id',dataIndex :'id', width:40}
#            ,{title : '当前状态',dataIndex :'applystatus', width:100}
#            ,{title : '申请人',dataIndex :'applyuser', width:100}
#            ,{title : '申请后台',dataIndex :'applyrole', width:120}
#            ,{title : '申请内容',dataIndex : 'applyvalue',width:240,renderer: Format.cutTextRenderer(30)}
#            ,{title : '申请时间',dataIndex :'applytime', width:130}
#            ,{title : '审批人',dataIndex :'approver', width:100}
#            ,{title : '审批时间',dataIndex :'approvetime', width:130}
#            ,{title : '操作',dataIndex : 'editurl',elCls : 'center',width:50}
#           '''
#    grid_format["grid_style"]=""",bbar:{pagingBar:true}"""
#    grid_format["store_style"]=""",pageSize:20"""
#    #htmlstr, js_file, css_file, html_footer=apply_list()
#    return fmt_html.bui.make_static_grid(rows,columns,0,grid_format)


def apply_token_audit(token):
    tokenlist = token.split('|')
    if len(tokenlist) > 4:
        applyid = int(tokenlist[0])
        oldstatus = int(tokenlist[1])
        newstatus = int(tokenlist[2])
        ownertoken = str(tokenlist[3])
        owner = str(tokenlist[4])
        if oldstatus == 1:
            sqlstr = "select approver from apply_list where id=%s and applystatus=1 and applytoken=%s"
        # elif oldstatus==2:
        #    sqlstr = "select dbatoken from apply_list where id=%s and applystatus=2 and dbatoken=%s"
        rows, columsn, localreslut = getResultSQL_para(
            sqlstr, (applyid, ownertoken))
        if len(rows) == 0:
            return "验证失败：token已使用或id状态已变更"
        else:
            changestatus(applyid, oldstatus, newstatus,
                         {"username": owner}, False)
            return "验证成功，该条审批信息已更新"
    else:
        return "失败：token不符合要求"


def apply_token_makesend(applyid, nowstatus):
    sqlstr = "select applyuser,applyname,applytype,applyrole,applyreason,applytime,approver,approvetime,dotime,applytoken,sectoken from apply_list where id=%s and applystatus=%s"
    rows, columsn, localreslut = getResultSQL_para(
        sqlstr, (applyid, nowstatus))
    print(len(rows))
    if len(rows) == 1:
        applyuser, applyname, applytype, applyrole, applyreason, applytime, approver, approvetime, dotime, applytoken, sectoken = rows[
            0]
        if nowstatus == 1:
            tokenkey = applytoken
            tokenuser = approver
        elif nowstatus == 2:
            tokenkey = applytoken
            tokenuser = "sec"
        keystr_ok = "%s|%s|%s|%s|%s" % (
            applyid, nowstatus, nowstatus + 1, tokenkey, tokenuser)
        print(keystr_ok)
        keystr_er = "%s|%s|-%s|%s|%s" % (applyid,
                                         nowstatus, nowstatus + 1, tokenkey, tokenuser)
        applyvalue1 = decode_applyvalue1(applyrole)

        mailtitle = "%s:%s权限申请审批%s" % (
            applytype, applyuser, {1: "等待审批", 2: "等待开通"}.get(nowstatus, ""))
        if nowstatus == 1:
            mailcontent = """
            <table>
            <tr><td><strong>申请人</strong></td><td>{applyuser}</td></tr>
            <tr><td><strong>姓名</strong></td><td>{applyname}</td></tr>
            <tr><td><strong>申请后台</strong></td><td>{applytype}</td></tr>
            <tr><td><strong>申请内容</strong></td><td>{applyrole}</td></tr>
            <tr><td><strong>申请时间</strong></td><td>{applytime}</td></tr>
            <tr><td><strong>申请原因</strong></td><td>{applyreason}</td></tr>
            <tr><td><strong>审批人</strong></td><td>{approver}</td></tr>
            <tr><td><strong>审批时间</strong></td><td>{approvetime}</td></tr>
            <tr><td>&nbsp;</td><td><a href="http://water.qudian.com/face.html?action=apply_audit&token={keystr_ok}"><span class="f_green">同意</span></a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="http://water.qudian.com/face.html?action=apply_audit&token={keystr_er}"><span class="f_green">拒绝</span></a></td></tr>
            </table>
            """.format(applyrole=applyrole, applyuser=applyuser, applyname=applyname, keystr_er=keystr_er, keystr_ok=keystr_ok, applytime=applytime, applyreason=applyreason, applytype=applytype, approver=approver, approvetime=approvetime)
        elif nowstatus == 2:
            mailcontent = """
            <table>
            <tr><td><strong>申请人</strong></td><td>{applyuser}</td></tr>
            <tr><td><strong>姓名</strong></td><td>{applyname}</td></tr>
            <tr><td><strong>申请后台</strong></td><td>{applytype}</td></tr>
            <tr><td><strong>申请内容</strong></td><td>{applyrole}</td></tr>
            <tr><td><strong>申请时间</strong></td><td>{applytime}</td></tr>
            <tr><td><strong>申请原因</strong></td><td>{applyreason}</td></tr>
            <tr><td><strong>审批人</strong></td><td>{approver}</td></tr>
            <tr><td><strong>审批时间</strong></td><td>{approvetime}</td></tr>
            </table>
            """.format(applyrole=applyrole, applyuser=applyuser, applyname=applyname, keystr_er=keystr_er, keystr_ok=keystr_ok, applytime=applytime, applyreason=applyreason, applytype=applytype, approver=approver, approvetime=approvetime)
        mailto = "%s@qudian.com" % (tokenuser,)
        print(mailto)
        mana_login().sendmail(mailto, mailtitle, mailcontent)
        return True
    else:
        return False


def changestatus(applyid, applystatus, newapplystatus, userinfo, checkperson=True):
    username = userinfo.get("username", "Na")
    if abs(newapplystatus) == 2:
        sqlstr = "update apply_list set applystatus=%s,approvetime=now() where approver=%s and  id=%s and applystatus=%s "
        paras = (newapplystatus, username, applyid, applystatus)

    elif abs(newapplystatus) == 9:
     #   if checkperson and int(userinfo.get("userpower",0))<100:
     #       return False
        sqlstr = "update apply_list set applystatus=%s,secuser=%s,dotime=now() where id=%s"
        paras = (newapplystatus, username, applyid)

    # elif newapplystatus==-1:
    #    sqlstr = "update apply_list set applystatus=%s,dbatime=now() where adduser=%s and  id=%s and applystatus=%s"
    exec_result, dic_result = exe_sql_para(sqlstr, paras)
    if newapplystatus == 2:
        apply_token_makesend(applyid, 2)
    # elif newapplystatus==9:
    #    apply_run.delay(applyid)
    return exec_result


def face_action(request):
    action = request.GET.get('action', "")
    dic_html = {'htmlstr': ''}
    # if action=="insert_mysql_proxy_port":
    #    dic_html['titlestr']=pub_def.insert_mysql_proxy_port(request.GET.get("value",''))
    if action == "apply_audit":
        token = request.GET.get('token', '')
        dic_html['titlestr'] = apply_token_audit(token)
    else:
        dic_html['titlestr'] = "%s action NOT FOUND" % (action,)
    return render(request, 'simple.html', dic_html)


def exe_sql_para(sqlstr, paras, iswait=False):
    connection = MySQLdb.connect(
        host='localhost', port=3306, user='root', passwd='hehe', db='djangoDB')
    connection.set_character_set('utf8')
    cursor = connection.cursor()
    step_starttime = time.time()
    sqlstrlist = sqlstr.split(";")
    for sqlstr_real in sqlstrlist:
        if len(sqlstr_real) > 5:
            cursor.execute(sqlstr_real, paras)
            if iswait:
                while cursor.nextset():
                    pass
            connection.commit()
    cursor.close()
    select_times = {'runtimes': int((time.time() - step_starttime) * 1000)}
    connection.close()
    return True, select_times


@login_required
def fuckadmin(request):
    mana_login = pub_def.mana_login()

    res_flag, res_num, res_info = mana_login.checkuserToken(request, 1)
    if res_flag == False:
        redirect('/login.html')

    userinfo = mana_login.get_userinfo(request)
    session_username = userinfo.get("username", "")
    if session_username in ['', '']:
        headstr = """<div style="margin-bottom:5px;">管理所有权限申请</a></div>"""
        htmlstr_list, js_file_list, css_file_list, html_footer_list = fuckadmin_html(
            request)
        dic_html = {}
        js_file = js_file_list
    #addr_to = list(set(js_file))
    # addr_to.sort(key=js_file.index)
        dic_html["title"] = "申请列表"
        dic_html["jsfile"] = "\n".join(js_file)
        dic_html["cssfile"] = ""
        dic_html["htmlstr"] = '%s\n<div style="width:1550px">%s</div>' % (
            headstr, htmlstr_list)
        dic_html["script_footer"] = html_footer_list
        return render(request, 'view_base.html', dic_html)
    else:
        return render(request, 'no.html')


@login_required
def fuckadmin_html(request):
    userinfo = mana_login().get_userinfo(request)
    username = userinfo.get("username", "")
    #username = replace_chart(request.GET.get('username', ''))
    sqlstr = """select id,applyuser,applyname,applytype,applymobile,applyrole,case when applystatus=1 then '新申请'
when applystatus=2 then '<span class="label label-info">已审批</span>'
when applystatus=-2 then '<span class="label label-warning">已拒绝</span>'
when applystatus=9 then '<span class="label label-success">流程成功</span>'
when applystatus=-9 then '<span class="label label-important">流程失败</span>' end as applystatus
,applytime,approver,approvetime,secuser,dotime,concat('<a href="mysqlaccoutinfo_add.html?id=',id,'">详细</a>') as editurl,concat('<div style="margin-bottom:5px;"><a href="fuckadmin_finish.html?id=',id,'" class="button button-small"><i class="icon-plus"></i>完成</a></div>') as editbutton,concat('<div style="margin-bottom:5px;"><a href="fuckadmin_bye.html?id=',id,'" class="button button-small"><i class="icon-plus"></i>拒绝</a></div>') as editbutton1 from apply_list order by id desc"""
    rows, columns, select_times = getResultSQL(sqlstr)
    grid_format = {}
    grid_format["columns"] = '''
            {title : 'id',dataIndex :'id', width:40}
            ,{title : '申请人',dataIndex :'applyuser', width:100}
            ,{title : '姓名',dataIndex :'applyname', width:100}
            ,{title : '申请后台',dataIndex :'applytype', width:80}
            ,{title : '手机号',dataIndex :'applymobile', width:100}
            ,{title : '当前状态',dataIndex :'applystatus', width:100}
            ,{title : '申请权限',dataIndex : 'applyrole',width:240,renderer: Format.cutTextRenderer(30)}
            ,{title : '申请时间',dataIndex :'applytime', width:130}
            ,{title : '审批人',dataIndex :'approver', width:100}
            ,{title : '审批时间',dataIndex :'approvetime', width:130}
            ,{title : '处理人',dataIndex :'secuser', width:100}
            ,{title : '完成时间',dataIndex :'dotime', width:130}
            ,{title : '操作',dataIndex : 'editurl',elCls : 'center',width:50}
            ,{title : '完成',dataIndex : 'editbutton',elCls : 'center',width:100}
            ,{title : '拒绝',dataIndex : 'editbutton1',elCls : 'center',width:100}
           '''
    grid_format["grid_style"] = """,bbar:{pagingBar:true}"""
    grid_format["store_style"] = """,pageSize:20"""
    #htmlstr, js_file, css_file, html_footer=apply_list()
    return fmt_html.bui.make_static_grid(rows, columns, 0, grid_format)


@login_required
def fuckadmin_finish(request):
    applyid = int(request.GET.get("id", "0"))
    applystatus = 2
    newapplystatus = 9
    userinfo = mana_login().get_userinfo(request)

    sqlstr = "select applyuser,applyname,applytype,applymobile,applyrole,applyreason,applytime,approver,approvetime from apply_list where id=%s"
    rows, columsn, localreslut = getResultSQL_para(sqlstr, (str(applyid),))
    if len(rows) == 1:
        applyuser, applyname, applytype, applymobile, applyrole, applyreason, applytime, approver, approvetime = rows[
            0]
        applyrole = decode_applyvalue1(applyrole)
        email = '邮箱'
        email = decode_applyvalue1(email)
        change_db_result = change_db(
            applyuser, applyname, applytype, applymobile, applyrole, str(applyid))
        if change_db_result == 0:
            change_result = changestatus(
                applyid, applystatus, newapplystatus, userinfo)
            if change_result:
                password_sql = 'select password from apply_list where id=%s'
                rows, columsn, localreslut = getResultSQL_para(
                    password_sql, (str(applyid),))
                if len(rows) == 1:
                    password = rows[0][0]
                    print password
                    if password == '0':
                        password = '已存在auth账号，请使用原有账号登录'
                        password = decode_applyvalue1(password)
                    mailcontent = """
                    <table>
                    <tr><td><strong>申请人</strong></td><td>{applyuser}</td></tr>
                    <tr><td><strong>姓名</strong></td><td>{applyname}</td></tr>
                    <tr><td><strong>申请后台</strong></td><td>{applytype}</td></tr>
                    <tr><td><strong>手机号</strong></td><td>{applymobile}</td></tr>
                    <tr><td><strong>申请内容</strong></td><td>{applyrole}</td></tr>
                    <tr><td><strong>申请时间</strong></td><td>{applytime}</td></tr>
                    <tr><td><strong>申请原因</strong></td><td>{applyreason}</td></tr>
                    <tr><td><strong>审批人</strong></td><td>{approver}</td></tr>
                    <tr><td><strong>审批时间</strong></td><td>{approvetime}</td></tr>
                    <tr><td><strong>用户名</strong></td><td>{email}</td></tr>
                    <tr><td><strong>密码</strong></td><td>{password}</td></tr>
                    </table>
                    """.format(email=email, password=password, applyrole=applyrole, applyuser=applyuser, applyname=applyname, applymobile=applymobile, applytime=applytime, applyreason=applyreason, applytype=applytype, approver=approver, approvetime=approvetime)
                pub_def.mana_login().sendmail(applyuser + '@qudian.com', '权限已开通', mailcontent)
                return render(request, 'ok.html')

        elif change_db_result == -3:
            change_result = changestatus(
                applyid, applystatus, newapplystatus, userinfo)
            if change_result:
                mailcontent = """
                <table>
                <tr><td><strong>申请人</strong></td><td>{applyuser}</td></tr>
                <tr><td><strong>姓名</strong></td><td>{applyname}</td></tr>
                <tr><td><strong>申请后台</strong></td><td>{applytype}</td></tr>
                <tr><td><strong>手机号</strong></td><td>{applymobile}</td></tr>
                <tr><td><strong>申请内容</strong></td><td>{applyrole}</td></tr>
                <tr><td><strong>申请时间</strong></td><td>{applytime}</td></tr>
                <tr><td><strong>申请原因</strong></td><td>{applyreason}</td></tr>
                <tr><td><strong>审批人</strong></td><td>{approver}</td></tr>
                <tr><td><strong>审批时间</strong></td><td>{approvetime}</td></tr>
                </table>
                """.format(applyrole=applyrole, applyuser=applyuser, applyname=applyname, applymobile=applymobile, applytime=applytime, applyreason=applyreason, applytype=applytype, approver=approver, approvetime=approvetime)
                pub_def.mana_login().sendmail(applyuser + '@.com', '权限已开通', mailcontent)
                return render(request, 'ok.html')

        else:
            return render(request, 'err.html')


@login_required
def fuckadmin_bye(request):
    applyid = int(request.GET.get("id", "0"))
    applystatus = 2
    newapplystatus = -9
    userinfo = mana_login().get_userinfo(request)
    change_result = changestatus(
        applyid, applystatus, newapplystatus, userinfo)
    if change_result:
        sqlstr = "select applyuser,applyname,applytype,applymobile,applyrole,applyreason,applytime,approver,approvetime,secuser,dotime from apply_list where id=%s"
        rows, columsn, localreslut = getResultSQL_para(sqlstr, (str(applyid),))
        if len(rows) == 1:
            applyuser, applyname, applymobile, applytype, applyrole, applyreason, applytime, approver, approvetime, secuser, dotime = rows[
                0]
            applyrole = decode_applyvalue1(applyrole)
            mailcontent = """
            <table>
            <tr><td><strong>申请人</strong></td><td>{applyuser}</td></tr>
            <tr><td><strong>姓名</strong></td><td>{applyname}</td></tr>
            <tr><td><strong>申请后台</strong></td><td>{applytype}</td></tr>
            <tr><td><strong>手机号</strong></td><td>{applymobile}</td></tr>
            <tr><td><strong>申请内容</strong></td><td>{applyrole}</td></tr>
            <tr><td><strong>申请时间</strong></td><td>{applytime}</td></tr>
            <tr><td><strong>申请原因</strong></td><td>{applyreason}</td></tr>
            <tr><td><strong>审批人</strong></td><td>{approver}</td></tr>
            <tr><td><strong>审批时间</strong></td><td>{approvetime}</td></tr>
            <tr><td><strong>处理人</strong></td><td>{secuser}</td></tr>
            <tr><td><strong>完成时间</strong></td><td>{dotime}</td></tr>
            </table>
            """.format(applyrole=applyrole, applyuser=applyuser, applyname=applyname, applymobile=applymobile, applytime=applytime, applyreason=applyreason, applytype=applytype, approver=approver, approvetime=approvetime, secuser=secuser, dotime=dotime)
        pub_def.mana_login().sendmail(applyuser + '@qudian.com', '权限申请被拒绝', mailcontent)
        return render(request, 'ok.html')


# 直接更新DB开通权限
def insert_user_role(applytype, applyrole, applymobile, proj_id):
    print 'insert user role'

    ap = applyrole.split(',')
    for p in ap:
        print p
        connection_w = MySQLdb.connect(host='', port=3306,
                                       user='', passwd='', db='permissions')
        connection_w.set_character_set('utf8')
        cursor = connection_w.cursor()
        try:
            insert_sql = 'insert into user_role (role_id,user_id) select a.id as rid,b.id as uid from (select id from role where role_name = %s and proj_id = %s) a  join (select id from user where phone = %s and is_delete=0)b;'
            cursor.execute(insert_sql, (p, proj_id, applymobile,))
            cursor.close()
            connection_w.commit()
            connection_w.close()
            print p + ' insert done!'
        except Exception, e:
            connection_w.rollback()
            connection_w.close()
            print e


def update_apply_user(name, phone, email, password, applyid):
    connection = MySQLdb.connect(
        host='localhost', port=3306, user='root', passwd='hehe', db='djangoDB')
    cursor = connection.cursor()
    try:
        sql = 'update apply_list set password=%s where id =%s'
        cursor.execute(sql, (password, applyid,))
        cursor.close()
        connection.commit()
    except Exception, e:
        connection.rollback()
        print e
    connection.close()


def gensecret(length):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])


def insert_user(applyuser, applyname, applymobile, applyid):
    print 'insert user'
    connection_w = MySQLdb.connect(host='', port=3306,
                                   user='', passwd='', db='permissions')
    connection_w.set_character_set('utf8')
    cursor = connection_w.cursor()
    secret = gensecret(12)
    secret = secret.encode('utf-8')
    passwd = bcrypt.hashpw(secret, bcrypt.gensalt(10)).replace('$2b$', '$2y$')
    name = applyname
    phone = applymobile
    email = applyuser + "@qudian.com"
    try:
        insert_sql = 'insert into user (name,phone,email,password) values(%s,%s,%s,%s);'
        cursor.execute(insert_sql, (name, phone, email, passwd,))
        cursor.close()
        connection_w.commit()
        connection_w.close()
        update_apply_user(name, phone, email, secret, applyid)
        return 1
    except Exception, e:
        connection_w.rollback()
        connection_w.close()
        print e
        return -1


def insert_user_proj(applytype, applymobile, proj_id):
    print 'insert user proj'
    connection_w = MySQLdb.connect(host='', port=3306,
                                   user='', passwd='', db='permissions')
    connection_w.set_character_set('utf8')
    cursor = connection_w.cursor()
    try:
        insert_sql = 'insert into user_proj (proj_id,user_id) values(%s,(select id from user where phone = %s and is_delete=0));'
        cursor.execute(insert_sql, (proj_id, applymobile,))
        cursor.close()
        connection_w.commit()
        connection_w.close()
        return 1
    except Exception, e:
        connection_w.rollback()
        connection_w.close()
        print e
        return -1


def check_user(applymobile):
    print 'check user'
    connection_r = MySQLdb.connect(host='',
                                   port=3306, user='', passwd='', db='permissions')
    connection_r.set_character_set('utf8')
    cursor = connection_r.cursor()
    try:
        check_user_sql = "select count(*) from user where phone = %s and is_delete=0"
        result = cursor.execute(check_user_sql, (applymobile,))
        r = cursor.fetchall()
        num = r[0][0]
        print 'user number: ' + str(num)
        cursor.close()
        connection_r.close()
        return num
    except Exception, e:
        connection_r.close()
        print e
        return -1


def check_proj(applymobile, applytype, proj_id):
    print 'check proj'
    connection_r = MySQLdb.connect(host='',
                                   port=3306, user='', passwd='', db='permissions')
    connection_r.set_character_set('utf8')
    cursor = connection_r.cursor()
    try:
        check_proj_sql = "select count(*) from user_proj where user_id = (select id from user where phone = %s and is_delete=0) and proj_id = %s;"
        result = cursor.execute(check_proj_sql, (applymobile, proj_id,))
        r = cursor.fetchall()
        num = r[0][0]
        print 'project number: ' + str(num)
        cursor.close()
        connection_r.close()
        return num
    except Exception, e:
        connection_r.close()
        print e
        return -1


def change_db(applyuser, applyname, applytype, applymobile, applyrole, applyid):
    print '-' * 50
    print 'change db'
    err = 0
    proj_id = {str("质检中心"): 29, str("MS后台"): 11, str("数据仓库"): 1, str("呼叫中心"): 3, str("营销中心"): 12, str("催收系统"): 16, str(
        "风控后台"): 7, str("支付管理后台"): 9, str("资金管理后台"): 15, str("BI工具后台"): 14, str("BI管理后台"): 19, str("监控后台"): 10}.get(applytype, 0)
    if proj_id != 0:
        c = check_user(applymobile)
        if c == 1:
            c_p = check_proj(applymobile, applytype, proj_id)
            if c_p == 1:
                insert_user_role(applytype, applyrole, applymobile, proj_id)
            elif c_p == 0:
                i_u_p = insert_user_proj(applytype, applymobile, proj_id)
                if i_u_p == 1:
                    print 'insert user proj done!'
                    insert_user_role(applytype, applyrole,
                                     applymobile, proj_id)
                else:
                    print 'insert user proj error!'
            else:
                print 'check user project error!'
                err = -1
        elif c == 0:
            i_u = insert_user(applyuser, applyname, applymobile, applyid)
            if i_u == 1:
                print 'insert user done!'
                i_u_p = insert_user_proj(applytype, applymobile, proj_id)
                if i_u_p == 1:
                    print 'insert user proj done!'
                    insert_user_role(applytype, applyrole,
                                     applymobile, proj_id)
                else:
                    print 'insert user proj error!'
        else:
            print 'check_user = ' + str(c)
            err = -2
    else:
        err = -3
        print 'no this project!'
    print 'done!'
    print '-' * 50
    return err
