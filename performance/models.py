from django.db import models
import django.utils.timezone as timezone


class ProjectInformation(models.Model):
    Project_Name_Choices = (
            ('CP1_TEST', 'CP1_TEST'),
            ('CP2_TEST', 'CP2_TEST'),
            ('CP3_TEST', 'CP3_TEST'),
            )
    Project_ID_Choices = (
            ('1D', '1D'),
            ('2D', '2D'),
            ('3D', '3D'),
            )
    # every test only concerntrate certain cpu type, so can not 
    # add it into "Hardwareenvironment"
    CPU_Type_Choices = (
            ('CPU 1.0', 'CPU 1.0'),
            ('CPU 1.1', 'CPU 1.1'),
            )
    project_name = models.CharField('Project Name',
            choices=Project_Name_Choices, max_length=32)
    project_id = models.CharField('Project ID', 
            choices=Project_ID_Choices, max_length=32)
    cpu_type = models.CharField('CPU Type',
            choices=CPU_Type_Choices, max_length=32, default='CPU 1.0'
            )
    reference_link = models.URLField('Reference Link (Confluence)',
            default='http://10.100.8.185:8090')

    class Meta:
        abstract = True


class HardwareEnvironment(models.Model):
    """
    Store Base Hardware Information.
    """

    # TODO: When modify "Hardwareenvironment", Please Remember 
    # Changing "Webservinghardwareenvironment" At the same time
    Machine_Name_Choices = (
            #(None, 'Choose Machine Name'),
            ('Habonaro', 'Habonaro'),
            ('Palmetto', 'Palmetto'),
            ('S812L', 'S812L'),
            ('S822L', 'S822L'),
            ('X86_E5', 'X86 E5 Series'),
            )
    Architecture_Type_Choices = (
            #(None, 'Choose Architecture Type'),
            ('x86', 'x86'),
            ('powerpc', 'powerpc'),
            ('arm64', 'arm64'),
            ('mips', 'mips'),
            )
    Byte_Order_Choices = (
            #(None, 'Litter or Big Endian'),
            ('litter_endian', 'Litter Endian'),
            ('big_endian', 'Big Endian'),
            )
    Machine_Side_Choices = (
            #(None, 'Server or Client Side'),
            ('server_side', 'As a Server'),
            ('client_side', 'As a Client'),
            )

    machine_side = models.CharField('Server/Client',
            choices=Machine_Side_Choices, max_length=32, default='server_side'
            )
    machine_name = models.CharField('Machine Name',
            choices=Machine_Name_Choices, max_length=32, default='Habonaro'
            )
    architecture_type = models.CharField('Architecture',
            choices=Architecture_Type_Choices, max_length=32,
            default='powerpc',
            )
    byte_order = models.CharField('Litter or Big endian',
            choices=Byte_Order_Choices, max_length=32, default='big_endian'
            )
    cpu_frequency = models.FloatField('CPU Clock Rate (GHZ)')
    l1_instruction = models.PositiveSmallIntegerField('L1 I-Cache (KB)')
    l1_data = models.PositiveSmallIntegerField('L1 D-Cache (KB)')
    l2 = models.PositiveSmallIntegerField('L2 Cache (KB)')
    l3 = models.PositiveIntegerField('L3 Cache (KB)', default=0, blank=True)
    l4 = models.PositiveIntegerField('L4 Cache (KB)', default=0, blank=True)
    memory = models.PositiveIntegerField('Memory (GB)')

    class Meta:
        abstract = True


class SoftwareEnvironment(models.Model):
    OS_Type_Choices = (
            ('Ubuntu 14.04.1', 'Ubuntu 14.04.1'),
            ('Ubuntu 14.04.2', 'Ubuntu 14.04.2'),
            ('Ubuntu 14.04.3', 'Ubuntu 14.04.3'),
            ('Ubuntu 14.04.10', 'Ubuntu 14.04.10'),
            ('RHEL 7.0', 'RHEL 7.0'),
            ('CentOS 6.6', 'CentOS 6.6'),
            ('CentOS 6.7', 'CentOS 6.7'),
            ('CentOS 7.0', 'CentOS 7.0'),
            ('Fedora 22', 'Fedora 22'),
            ('PowerKVM 2.1.1', 'PowerKVM 2.1.1'),
            )
    kernel_version = (
            ('2.6.32-573.7.1.e16.centos.plus.x86_64',
                '2.6.32-573.7.1.e16.centos.plus.x86_64'),
            ('3.10.0-pagecoloring-cpufreq+', '3.10.0-pagecoloring-cpufreq+'),
            ('3.10.53-2025.1.pkvm2_1_1.54.ppc64',
                '3.10.53-2025.1.pkvm2_1_1.54.ppc64'),
            ('3.10.89-2045.1.pkvm2_1_1.74.ppc64',
                '3.10.89-2045.1.pkvm2_1_1.74.ppc64'),
            ('3.13.0-32-generic', '3.13.0-32-generic'),
            ('3.16.0-23-generic', '3.16.0-23-generic'),
            ('3.16.0-30-generic', '3.16.0-30-generic'),
            ('3.16.0-51-generic', '3.16.0-51-generic'),
            ('3.19.0-25-generic', '3.19.0-25-generic'),
            ('4.0.4-301.fc22.ppc64', '4.0.4-301.fc22.ppc64'),
            ('4.1.0-pagecoloring', '4.1.0-pagecoloring'),
            )
    os_type = models.CharField('Operation System', choices=OS_Type_Choices,
            max_length=64, default='Ubuntu 14.04.2')
    kernel_version = models.CharField('Kernel Version',
            choices=kernel_version, max_length=64, default='3.16.0-30-generic')
    dependence_information = models.TextField('Dependency Instruction',
            max_length=1024, blank=True)

    class Meta:
        abstract = True


class Bottleneck(models.Model):
    neck_cpu = models.BooleanField('CPU Neck')
    neck_io = models.BooleanField('IO Neck')
    neck_memory = models.BooleanField('Memory Neck')
    neck_net = models.BooleanField('Net Neck')

    class Meta:
        abstract = True



APPLICATIONS = ('Data Caching', 'Lmbench', 'Parsec', 'Sirius', 'Spark Terasort',
        'SPEC CPU', 'SPEC jbb', 'SPEC jvm', 'Splash', 'TPCC', 'WebServing', )

#####################       Application From Here          ###################
##############################################################################
class DataCachingInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Data Caching',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_max_rps = models.FloatField('Result - Max RPS')
    data_scale = models.PositiveSmallIntegerField('Data Scale')
    number_works = models.PositiveSmallIntegerField('Work Number')
    number_connections = models.PositiveSmallIntegerField('Connection Number')
    number_threads = models.PositiveSmallIntegerField('Thread Number')
    network_bandwidth_datacaching = models.PositiveSmallIntegerField(
            'Network Bandwidth (Mbps)')

    def __str__(self):
        return "{0}: Max RPS={1} | Data Scale={2} | Works={3} | "\
    "Connections={4} | Threads={5} | Network Bandwidth={6}".format(
            self.test_application, self.result_max_rps, self.data_scale,
            self.number_works,self.number_connections, self.number_threads,
            self.network_bandwidth_datacaching)

    class Meta:
        abstract = False


class DataCachingMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(DataCachingInformation,
            verbose_name='DataCaching Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class LmbenchInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Lmbench',
            editable=False)
    version = models.CharField('Application Version', max_length = 10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.FloatField('Result - Time')
    app_name_lmbench = models.CharField('app name', max_length=256, default='bw_mem')
    problem_size = models.CharField('Problem Size', max_length=256)
    thread_number_lmbench = models.CharField('Thread Number', max_length=256)
    node = models.CharField('Node', max_length=256)
    phycpu = models.CharField('Physical CPU', max_length=256)
    stride_size = models.PositiveIntegerField('Stride Size (Byte)')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Problem Size={3} | Thread'\
    ' Number={4} | Node={5} | Physical CPU={6} | Stride Size={7}'.format(
            self.test_application, self.result_time, self.app_name_lmbench, 
            self.problem_size, self.thread_number_lmbench, self.node, self.phycpu,
            self.stride_size)

    class Meta:
        abstract = False


class LmbenchMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(LmbenchInformation,
            verbose_name='Lmbench Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class ParsecInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Parsec',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.FloatField('Result - Time(s)')
    app_name_parsec = models.CharField('app name', max_length=256)
    input_set = models.CharField('Input Set', max_length=256)
    thread_number_parsec = models.PositiveSmallIntegerField('Thread Number')
    smt_number = models.PositiveSmallIntegerField('SMT')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Input Set={3} | Threads={4} |'\
    ' SMT={5}'.format(self.test_application, self.result_time,
            self.app_name_parsec, self.input_set, self.thread_number_parsec, 
            self.smt_number)

    class Meta:
        abstract = False


class ParsecMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(ParsecInformation,
            verbose_name='Parsec Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SiriusSuitInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Sirius-suit',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_run_time = models.FloatField('Result - RUN_TIME(ms)')
    result_passed = models.BooleanField('Result - PASSED')
    result_warnings = models.BooleanField('Result - WARNINGS')
    result_errors = models.BooleanField('Result - ERRORS')
    app_name_siriussuit = models.CharField('app name', max_length=256)
    pthread_num = models.PositiveSmallIntegerField('Pthread Number')
    dataset_size = models.FloatField('Dataset Size (GB)')

    def __str__(self):
        return '{0}: Run Time{1} | PASSED={2} | WARNINGS={3} | ERRORS={4} | '\
    'app name={5} | Pthread={6} | Dataset={7} GB'.format(
            self.test_application, self.result_run_time, self.result_passed,
            self.result_warnings, self.result_errors, self.app_name_siriussuit,
            self.pthread_num, self.dataset_size)

    class Meta:
        abstract = False


class SiriusSuitMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SiriusSuitInformation,
            verbose_name='Sirius-suit Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SparkTerasortInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spark Terasort',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.FloatField('Result - Time(s)')
    data_size = models.FloatField('Data Size (GB)')
    partition_size = models.PositiveSmallIntegerField('Partition Size')
    processor_number = models.PositiveSmallIntegerField('Processor Number')
    workers = models.PositiveIntegerField('Workers')

    def __str__(self):
        return '{0}: Time(s)={1} | Data Size={2} | Partition Size={3} | '\
    'Processor Number={4} | Works={5}'.format(self.test_application,
            self.result_time, self.data_size, self.partition_size,
            self.processor_number, self.workers)

    class Meta:
        abstract = False


class SparkTerasortMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SparkTerasortInformation,
            verbose_name='SparkTerasort Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SpecCPUInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='SPEC CPU',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_int_rate_ratio = models.FloatField("Result - INT Rate Ratio's")
    result_fp_rate_ratio = models.FloatField("Result - FP Rate Ratio's")
    benchmarks = models.CharField("Benchmarks", max_length=256)
    copies = models.PositiveSmallIntegerField('Copies')
    smt_number = models.PositiveSmallIntegerField('SMT')

    def __str__(self):
        return "{0}: INT Rate Ratio's={1} | FP Rate Ratio's={2} |"\
    " Benchmarks={3} | Copies={4} | SMT={5}".format(self.test_application,
            self.result_int_rate_ratio, self.result_fp_rate_ratio,
            self.benchmarks, self.copies, self.smt_number)

    class Meta:
        abstract = False


class SpecCPUMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    threads_per_core = models.PositiveSmallIntegerField('Thread(s) Per Core')
    cores_per_socket = models.PositiveSmallIntegerField('Core(s) Per Socket')
    socket_number = models.PositiveSmallIntegerField('Socket(s)')
    numa_nodes = models.PositiveSmallIntegerField('NUMA Node(s)')
    cpu_number = models.PositiveSmallIntegerField('CPU(s)')
    app_information = models.ForeignKey(SpecCPUInformation,
            verbose_name='SPEC CPU Information')
    half_l3_speccpu = models.BooleanField('Half L3 Cache', default=False)
    existing_l4_speccpu = models.BooleanField('Open L4 Cache', default=True)

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SpecjbbInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spec jbb',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2005')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_bops = models.FloatField('Result - bops')
    # the jbb_attachment is a part of result in Specjbb
    jbb_attachment = models.FileField(upload_to = '%Y-%m-%d/%H-%M-%S',
            blank=True)
    app_name_specjbb = models.CharField('app name', max_length=256)
    processor_number = models.PositiveSmallIntegerField('Processor Number')
    jvm_parameter_specjbb = models.CharField('JVM Parameter', max_length=512)
    jvm_instances = models.PositiveSmallIntegerField('JVM Instances')
    warehouses = models.PositiveIntegerField('WAREHOUSES')

    def __str__(self):
        return '{0}: bops={1} | app name={2} | JVM Parameter={3} | '\
    'Processor(s)={4} | JVM Instances={5} | WAREHOUSES={6}'.format(
            self.test_application, self.result_bops, self.app_name_specjbb, 
            self.jvm_parameter_specjbb, self.processor_number,
            self.jvm_instances, self.warehouses)

    class Meta:
        abstract = False


class SpecjbbMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SpecjbbInformation,
            verbose_name='Specjbb Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SpecjvmInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spec jvm',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2008')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_bops = models.FloatField('Result - bops')
    jvm_attachment = models.FileField(upload_to = '%Y-%m-%d/%H-%M-%S',
            blank=True)
    app_name_specjvm = models.CharField('app name', max_length=256)
    jvm_parameter_specjvm = models.CharField('JVM Parameter', max_length=512)
    specjvm_parameter = models.CharField('Spec JVM Parameter', max_length=512)
    processor_number = models.PositiveSmallIntegerField('Processor Number')

    def __str__(self):
        return '{0}: bops={1} | app name={2} | JVM Parameter={3} | '\
    'Spec JVM Parameter={4} | processor_number={5}'.format(
            self.test_application, self.result_bops, self.app_name_specjvm,
            self.jvm_parameter_specjvm, self.specjvm_parameter, 
            self.processor_number)

    class Meta:
        abstract = False


class SpecjvmMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SpecjvmInformation,
            verbose_name='Specjvm Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class SplashInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Splash',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2.0')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.FloatField('Result - Time(us)')
    app_name_splash = models.CharField('app name', max_length=256)
    problem_size = models.CharField('Problem Size', max_length=256)
    processor_number = models.PositiveSmallIntegerField('Processor Number')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Problem Size={3} | '\
    'Processor={4}'.format(self.test_application, self.result_time,
            self.app_name_splash, self.problem_size, self.processor_number)

    class Meta:
        abstract = False


class SplashMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SplashInformation,
            verbose_name='Splash Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class TpccInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='TPC-C',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_tpmc = models.FloatField('Result - tpmC')
    warehouses = models.PositiveIntegerField('WAREHOUSES')
    terminals = models.PositiveSmallIntegerField('TERMINALS')
    run_time = models.FloatField('RUN_TIME')
    network_bandwidth_tpcc = models.PositiveSmallIntegerField(
            'Network Bandwidth (Mbps)')

    def __str__(self):
        return '{0}: tpmC={1} | WAREHOUSES={2} | TERMINALS={3} | Run '\
        'Time={4} | Network Bandwidth={5}'.format(self.test_application,
        self.result_tpmc, self.warehouses, self.terminals, self.run_time,
            self.network_bandwidth_tpcc)

    class Meta:
        abstract = False


class TpccMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(TpccInformation,
            verbose_name='TPC-C Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False


##############################################################################
class WebServingInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='WebServing',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_ops = models.FloatField('Result - OPS')
    result_passed = models.BooleanField('Result - PASSED')
    result_warnings = models.BooleanField('Result - WARNINGS')
    result_errors = models.BooleanField('Result - ERRORS')
    warm_up = models.PositiveSmallIntegerField('Warm Up')
    con_users = models.PositiveSmallIntegerField('CON Users')
    pm_static = models.BooleanField('PM Staic')
    pm_max_connections = models.PositiveSmallIntegerField(
            'PM Max Connections', default=0)
    sql_max_connections = models.PositiveSmallIntegerField(
            'SQL Max Connections')
    worker_processes = models.PositiveSmallIntegerField('Worker Processes')
    worker_connection = models.PositiveSmallIntegerField('Worker Connection')
    network_bandwidth_webserving = models.PositiveSmallIntegerField(
            'Network Bandwidth (Mbps)')

    def __str__(self):
        return '{0}: OPS={1} | PASSED={2} | WARNINGS={3} | ERRORS={4} | Warm'\
    ' Up={5} | CON Users={6} | PM Staic={7} | PM Max Connections={8} | '\
    'SQL Max Connections={9} | Worker Processes={10} | Worker Connection={11}'\
    ' | Network Bandwidth={12}'.format(self.test_application, self.result_ops,
            self.result_passed, self.result_warnings, self.result_errors,
            self.warm_up, self.con_users, self.pm_static,
            self.pm_max_connections, self.sql_max_connections,
            self.worker_processes, self.worker_connection,
            self.network_bandwidth_webserving)

    class Meta:
        abstract = False


class WebServingHardwareEnvironment(models.Model):
    Machine_Name_Choices = (
            #(None, 'Choose Machine Name'),
            ('Habonaro', 'Habonaro'),
            ('Palmetto', 'Palmetto'),
            ('S812L', 'S812L'),
            ('S822L', 'S822L'),
            ('X86_E5', 'X86 E5 Series'),
            )
    Architecture_Type_Choices = (
            #(None, 'Choose Architecture Type'),
            ('x86', 'x86'),
            ('powerpc', 'powerpc'),
            ('arm64', 'arm64'),
            ('mips', 'mips'),
            )
    Byte_Order_Choices = (
            #(None, 'Litter or Big Endian'),
            ('litter_endian', 'Litter Endian'),
            ('big_endian', 'Big Endian'),
            )
    Machine_Side_Choices = (
            ('frontend', 'As a Frontend'),
            ('backend', 'As a Backend'),
            ('client_side', 'As a Client'),
            )

    #TODO: django1.8 Can not override the field
    """
    There is a link about "Field name “hiding” is not permitted"
    https://docs.djangoproject.com/en/dev/topics/db/models/#field-name-hiding-is-not-permitted
    """
    machine_side = models.CharField('Machine Role',
            choices=Machine_Side_Choices, max_length=32, default='client_side'
            )
    machine_name = models.CharField('Machine Name',
            choices=Machine_Name_Choices, max_length=32, default='Habonaro'
            )
    architecture_type = models.CharField('Architecture',
            choices=Architecture_Type_Choices, max_length=32,
            default='powerpc'
            )
    byte_order = models.CharField('Litter or Big endian',
            choices=Byte_Order_Choices, max_length=32, default='big_endian'
            )
    cpu_frequency = models.FloatField('CPU Clock Rate (GHZ)')
    l1_instruction = models.PositiveSmallIntegerField('L1 I-Cache (KB)')
    l1_data = models.PositiveSmallIntegerField('L1 D-Cache (KB)')
    l2 = models.PositiveSmallIntegerField('L2 Cache (KB)')
    l3 = models.PositiveIntegerField('L3 Cache (KB)', default=0, blank=True)
    half_l3 = models.BooleanField('Half L3 Cache')
    l4 = models.PositiveIntegerField('L4 Cache (KB)', default=0, blank=True)
    memory = models.PositiveIntegerField('Memory (MB)')

    class Meta:
        abstract = True


class WebServingMachine(WebServingHardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(WebServingInformation,
            verbose_name='WebServing Information')

    def __str__(self):
        return "id={0} | app_information_id={1}".format(
            self.id, self.app_information_id)

    class Meta:
        abstract = False

