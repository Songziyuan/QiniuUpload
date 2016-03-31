from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import config
import os
import time
import conwebp


# 需要填写你的 Access Key 和 Secret Key

def upload(origin_file_path):
    # 构建鉴权对象
    q = Auth(config.access_key, config.secret_key)

    # 要上传的空间
    bucket_name = 'md-doc'
    localfile = conwebp.convert(origin_file_path)

    # 上传到七牛后保存的文件名
    dest_prefix = time.strftime("%Y%m%d%H%M%S", time.localtime())
    dest_name = dest_prefix + "_" + os.path.basename(localfile)

    # 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
    policy = {
        'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
    }

    token = q.upload_token(bucket_name, dest_name, 3600, policy)

    ret, info = put_file(token, dest_name, localfile)
    if ret is not None:
        print("Upload Success,url=", config.domin + dest_name)
    else:
        print("info=", info)
        print("ret=", ret)
    assert ret['key'] == dest_name
    assert ret['hash'] == etag(localfile)
