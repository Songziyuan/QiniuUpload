import shlex
import datetime
import subprocess
import time
import os


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # 没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)

    # subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)
    result = str(sub.returncode)
    return result


def needconvert(filepath):
    name, ext = os.path.split(filepath)
    # webp图片不再进行压缩
    if ext == '.webp':
        return False
    # 高保真图片需要压缩
    if ext == '.png' or ext == '.bmp':
        return True
    # 其他格式的压缩图片,当size小于50kb的时候,不压缩为webp(因为不能取得较好的效果)
    elif os.path.getsize(filepath) / 1024 < 50:
        return False
    else:
        return True


# 调用google的cwebp(https://developers.google.com/speed/webp/docs/cwebp#options)进行转换
def convert_webp(origin_file_path):
    name = os.path.basename(origin_file_path).split(".")[0]
    result_filename = '/tmp/' + name + '.webp'
    command = 'cwebp -q 80 ' + origin_file_path + ' -o ' + result_filename
    convert_result = execute_command(command)
    print(convert_result)
    return result_filename


# 调用ImageMagic(http://www.imagemagick.org/script/index.php)来优化Gif文件
def convert_gif(origin_file_path):
    name = os.path.basename(origin_file_path)
    result_filename = '/tmp/' + 'result_' + name
    command = 'convert ' + origin_file_path + ' -fuzz 5% -layers Optimize ' + result_filename
    convert_result = execute_command(command)
    print(convert_result)
    return result_filename


# 转化,基本业务逻辑如下:1,判断是否需要转换,如果不需要,则直接返回原始文件路径;2,如果是gif文件,则调用convert_gif转换;3,其他文件则调用convert_webp转换为webp文件
def convert(origin_file_path):
    if not needconvert(origin_file_path):
        return origin_file_path
    name, ext = os.path.split(origin_file_path)
    if ext == '.gif':
        return convert_gif(origin_file_path)
    else:
        return convert_webp(origin_file_path)


if __name__ == "__main__":
    print(execute_command("ls"))
