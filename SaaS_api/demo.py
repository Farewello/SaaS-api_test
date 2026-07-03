"""
批量删除知识库文件夹（批量操作工具）。

前置条件：config/config.yaml 中配置有效的账号密码。
Usage: python demo.py [start_id=726] [end_id=753]
"""

import sys
import requests
from api_module.BaseApi import BaseApi
from api_module.login import login
from common.global_env import get_env


def delete_kb_folder(folder_id: int, merchant_id: int, brand_id: int,
                     scope_id: int = 1234, kb_id: int = 758) -> requests.Response:
    """删除指定知识库文件夹"""
    return BaseApi().run_api(
        'kb_delete.yaml', 'delete_kb_folder',
        merchantId=merchant_id,
        brandId=brand_id,
        scopeId=scope_id,
        knowledgeBaseId=kb_id,
        id=folder_id,
    )


def list_kb_folders(merchant_id: int, brand_id: int,
                    scope_id: int = 1234, kb_id: int = 758) -> requests.Response:
    """列出知识库文件夹"""
    return BaseApi().run_api(
        'knowledge.yaml', 'create_kb_folder',
        merchantId=merchant_id,
        brandId=brand_id,
        scopeId=scope_id,
        knowledgeBaseId=kb_id,
        name='test_list_placeholder',
    )


if __name__ == '__main__':
    start_id = int(sys.argv[1]) if len(sys.argv) > 1 else 726
    end_id = int(sys.argv[2]) if len(sys.argv) > 2 else 753

    # 登录 → 获取 token + merchant_id
    print('正在登录...')
    login()

    merchant_id = get_env('merchant_id')
    if merchant_id is None:
        print('ERROR: 登录失败，merchant_id 未设置')
        sys.exit(1)

    # 获取品牌列表 → brand_id
    print('正在获取品牌列表...')
    from api_module.brand import get_brand_list
    get_brand_list()

    brand_id = get_env('brand_id')
    if brand_id is None:
        print('ERROR: 品牌列表为空')
        sys.exit(1)

    print(f'登录成功，merchant_id={merchant_id}, brand_id={brand_id}')
    print(f'准备批量删除知识库文件夹 {start_id} ~ {end_id} ...')

    success = 0
    fail = 0
    for fid in range(start_id, end_id + 1):
        try:
            resp = delete_kb_folder(fid, merchant_id, brand_id)
            body = resp.json()
            if body.get('returnCode') == '000000':
                print(f'  ✔ 删除 {fid} 成功')
                success += 1
            else:
                print(f'  ✘ 删除 {fid} 失败: {body.get("returnMsg", body)}')
                fail += 1
        except Exception as e:
            print(f'  ✘ 删除 {fid} 异常: {e}')
            fail += 1

    print(f'\n执行完毕：成功 {success}，失败 {fail}，共 {end_id - start_id + 1}')
