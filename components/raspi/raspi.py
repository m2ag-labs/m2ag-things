import psutil
import subprocess


class Raspi:

    def __init__(self):
        # Gather systemtype info
        pass

    def get(self, value):
        if value == 'cpu_temp':
            return self.get_cpu_temp()
        if value == 'cpu_freq':
            return self.get_cpu_freq()
        if value == 'serial':
            return self.get_serial_number()
        if value == 'system_type':
            return self.get_system_type()
        if value == 'hardware':
            return self.get_hardware()
        if value == 'revision':
            return self.get_revision()
        if value == 'os_info':
            return self.get_os_info()
        if value == 'arm_ver':
            return self.get_arm_ver()

    @staticmethod
    def get_cpu_temp():
        val = psutil.sensors_temperatures()
        try:
            return val['cpu_thermal'][0].current
        except KeyError:
            return val['cpu-thermal'][0].current

    @staticmethod
    def get_cpu_freq():
        val = psutil.cpu_freq()
        return val.current

    @staticmethod
    def get_system_type():
        p = subprocess.Popen(['/bin/cat', '/sys/firmware/devicetree/base/model'], stdout=subprocess.PIPE, )
        line = str(p.stdout.readline().decode('utf-8').rstrip())
        return line

    @staticmethod
    def get_serial_number():
        p1 = subprocess.Popen(['/bin/cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, )
        p2 = subprocess.Popen(['grep', 'Serial'], stdin=p1.stdout, stdout=subprocess.PIPE, )
        p3 = subprocess.Popen(['cut', '-d', ' ', '-f', '2'], stdin=p2.stdout, stdout=subprocess.PIPE, )
        p1.stdout.close()
        p2.stdout.close()
        line = p3.stdout.readline().decode('utf-8').rstrip()
        return hex(int(line, 16))

    @staticmethod
    def get_hardware():
        p1 = subprocess.Popen(['/bin/cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, )
        p2 = subprocess.Popen(['grep', 'Hardware'], stdin=p1.stdout, stdout=subprocess.PIPE, )
        p3 = subprocess.Popen(['cut', '-d', ' ', '-f', '2'], stdin=p2.stdout, stdout=subprocess.PIPE, )
        p1.stdout.close()
        p2.stdout.close()
        line = p3.stdout.readline().decode('utf-8').rstrip()
        return line

    @staticmethod
    def get_revision():
        p1 = subprocess.Popen(['/bin/cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, )
        p2 = subprocess.Popen(['grep', 'Revision'], stdin=p1.stdout, stdout=subprocess.PIPE, )
        p3 = subprocess.Popen(['cut', '-d', ' ', '-f', '2'], stdin=p2.stdout, stdout=subprocess.PIPE, )
        p1.stdout.close()
        p2.stdout.close()
        line = p3.stdout.readline().decode('utf-8').rstrip()
        return line

    @staticmethod
    def get_os_info():
        p1 = subprocess.Popen(['/bin/cat', '/etc/os-release'], stdout=subprocess.PIPE, )
        p2 = subprocess.Popen(['grep', 'PRETTY_NAME'], stdin=p1.stdout, stdout=subprocess.PIPE, )
        p3 = subprocess.Popen(['cut', '-d', '=', '-f', '2'], stdin=p2.stdout, stdout=subprocess.PIPE, )
        p1.stdout.close()
        p2.stdout.close()
        line = p3.stdout.readline().decode('utf-8').rstrip()
        return line

    @staticmethod
    def get_arm_ver():
        p1 = subprocess.Popen(['/bin/uname', '-a'], stdout=subprocess.PIPE, )
        line = p1.stdout.readline().decode('utf-8').rstrip()
        return line.split(' ')[11]

