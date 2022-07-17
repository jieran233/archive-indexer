import sys
import os
from subprocess import PIPE, Popen  # 执行系统命令
import pathlib


def executeCommandLine(cli):
    try:
        # 返回的是 Popen 实例对象
        proc = Popen(
            str(cli),  # cmd特定的查询空间的命令
            stdin=None,  # 标准输入 键盘
            stdout=PIPE,  # -1 标准输出（演示器、终端) 保存到管道中以便进行操作
            stderr=PIPE,  # 标准错误，保存到管道
            shell=True)

        # print(proc.communicate()) # 标准输出的字符串+标准错误的字符串
        outinfo, errinfo = proc.communicate()
        outinfo = outinfo.decode('gbk')
        errinfo = errinfo.decode('gbk')
        infos = {'outinfo': outinfo, 'errinfo': errinfo}
        # print(outinfo.decode('gbk'))  # 外部程序(windows系统)决定编码格式
        # print(errinfo.decode('gbk'))
        return infos
    except Exception as e:
        print('\033[0;31m' + str(e.args) + '\033[0m')
        return


class archive_indexer:
    def locate_bin(self, bin_='7z.exe'):
        is_64bits = sys.maxsize > 2 ** 32  # https://docs.python.org/zh-cn/3/library/platform.html
        if bin_ == '7z.exe':
            bin_files = [r'\bin\x86\7z.exe', r'\bin\amd64\7z.exe']
        elif bin_ == 'touch.exe':
            bin_files = [r'\bin\x86\touch.exe', r'\bin\amd64\touch.exe']
        script_directory = os.path.split(os.path.realpath(__file__))[0]  # https://blog.csdn.net/vitaminc4/article/details/78702852
        return(script_directory + bin_files[int(is_64bits)])

    def ls(self, archive_path):
        bin_path = self.locate_bin()
        cli = r'"{}" l -r "{}"'.format(bin_path, archive_path)
        print(cli)
        o = executeCommandLine(cli)['outinfo']
        print(o)
        o = o.splitlines()
        files = []
        attrs = []
        j = 0
        for i in range(len(o)):
            attr = o[i][20:25]
            s = o[i].split('  ')[-1]
            if s == '------------------------':
                j = j + 1
                # print('start/end')
            if j % 2 != 0:
                attrs.append(attr)
                files.append(s)
        attrs = attrs[1:]
        files = files[1:]
        r = {'attrs': attrs, 'files': files}
        return(r)
    # def mkfiles(self):

    def process_path(self, filepath, folders_or_files, mkdir):
        path_ = filepath.split('\\')[:-1]
        archive_name_ = filepath.split('\\')[-1].split('.')[:-1]
        archive_name = ''
        for i in range(len(archive_name_)):
            archive_name = archive_name + archive_name_[i] + '.'
        archive_name = archive_name[:-1]
        path = ''
        for i in range(len(path_)):
            path = path + path_[i] + '\\'
        if mkdir:
            # print(archive_name)
            return path + archive_name + '\\' + folders_or_files
        else:
            return path + folders_or_files

    def mkdir(self, filepath, folders, mkdir):
        for i in range(len(folders)):
            d = self.process_path(filepath, folders[i], mkdir)
            print('create dir: ' + d)
            try:
                os.makedirs(d)
            except Exception as e:
                print(e.args)

    def touch(self, filepath, files, mkdir):
        for i in range(len(files)):
            f = self.process_path(filepath, files[i], mkdir)
            print('create file: ' + f)
            try:
                pathlib.Path(f).touch()
            except Exception as e:
                print(e.args)
            # cli = r'"{}" "{}"'.format(self.locate_bin('touch.exe'), f)
            # # print(cli)
            # o = executeCommandLine(cli)
            # if o['errinfo'] != '':
            #     print(o['errinfo'])

    def main(self, filepath, mkdir):
        r = self.ls(filepath)
        attrs = r['attrs']
        files = r['files']

        Folders = []
        Files = []
        for i in range(len(files)):
            if attrs[i].find('D') != -1:  # Folder(s)
                Folders.append(files[i])
            elif attrs[i].find('A') != -1:  # File(s)
                Files.append(files[i])

        print('Folder(s) ({}): {}\n\nFile(s) ({}): {}'.format(str(len(Folders)), str(Folders), str(len(Files)), str(Files)))
        print('Creating Folder(s) (mkdir)...')
        self.mkdir(filepath, Folders, mkdir)
        print('Creating File(s) (touch)...')
        self.touch(filepath, Files, mkdir)


if __name__ == '__main__':
    if sys.platform != 'win32':
        exit()
    if len(sys.argv) < 2:
        exit()

    file = sys.argv[1]
    mkdir_ = False

    if len(sys.argv) == 3:
        switch = sys.argv[2]
        if switch == '--mkdir':
            mkdir_ = True

    idxer = archive_indexer()
    idxer.main(file, mkdir_)