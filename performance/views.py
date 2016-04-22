import os
import datetime
import copy
import math
import itertools
import collections

from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate
from .report_conf import h1_style, h2_style, h4_style
from .report_conf import insert_space, show_content, show_main_table, \
        show_conf_table, show_figure, insert_image

from .models import ProjectInformation
# from .models import HardwareEnvironment
from .models import DataCachingInformation as dc_i, DataCachingMachine as dc_m
from .models import LmbenchInformation as lb_i, LmbenchMachine as lb_m
from .models import ParsecInformation as pa_i, ParsecMachine as pa_m
from .models import SiriusSuitInformation as ss_i, SiriusSuitMachine as ss_m
from .models import SparkTerasortInformation as st_i, SparkTerasortMachine as \
        st_m
from .models import SpecCPUInformation as scpu_i, SpecCPUMachine as scpu_m
from .models import SpecjbbInformation as sjbb_i, SpecjbbMachine as sjbb_m
from .models import SpecjvmInformation as sjvm_i, SpecjvmMachine as sjvm_m
from .models import SplashInformation as spl_i, SplashMachine as spl_m
from .models import TpccInformation as tpc_i, TpccMachine as tpc_m
from .models import WebServingInformation as ws_i, WebServingMachine as ws_m
# from .models import WebServingHardwareEnvironment as ws_h


project_names = [i[0] for i in ProjectInformation.Project_Name_Choices]
# architectures = [i[0] for i in HardwareEnvironment.Architecture_Type_Choices]
cpu_types = [i[0] for i in ProjectInformation.CPU_Type_Choices]


class ApplicationBaseInformation(object):
    """
    This class store base information related to all applications include:
    "datacaching, lmbench, parsec, siriussuit, sparkterasort, speccpu,
    specjbb, specjvm, splash, tpcc and webserving".
    """
    def __init__(self):
        self.applications = ['datacaching', 'lmbench', 'parsec', 'siriussuit',
                             'sparkterasort', 'speccpu', 'specjbb', 'specjvm',
                             'splash', 'tpcc', 'webserving']
        self.app_infor = {}
        # TODO: I will add 'choice_fields_mach' for every application to
        # handle the extra fields from machine_module
        self.app_infor['datacaching'] = {
                'information_module': dc_i,
                'machine_module': dc_m,
                'multi_child_app': (False, ''),
                # machine_fields only fits for application who owns one machine
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('data_scale', 'number_works',
                                  'number_connections', 'number_threads',
                                  'network_bandwidth_datacaching'),
                'result_fields': ('result_max_rps', ),
                'best_result': 'max',
                'result_alias_fields': ('data_scale', 'number_works',
                                        'number_connections', 'number_threads',
                                        'network_bandwidth_datacaching',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['lmbench'] = {
                'information_module': lb_i,
                'machine_module': lb_m,
                'multi_child_app': (True, 'app_name_lmbench'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('node', 'phycpu', 'stride_size',
                                  'thread_number_lmbench'),
                'result_fields': ('result_time', ),
                'best_result': 'min',
                'result_alias_fields': ('thread_number_lmbench', 'node',
                                        'phycpu', 'stride_size',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['parsec'] = {
                'information_module': pa_i,
                'machine_module': pa_m,
                'multi_child_app': (True, 'app_name_parsec'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('thread_number_parsec', 'app_name_parsec',
                                  'input_set'),
                'result_fields': ('result_time', ),
                'best_result': 'min',
                'result_alias_fields': ('thread_number_parsec', 'input_set',
                                        'reference_link', 'app_name_parsec',
                                        'cpu_type'),
                }
        self.app_infor['siriussuit'] = {
                'information_module': ss_i,
                'machine_module': ss_m,
                'multi_child_app': (True, 'app_name_siriussuit'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('app_name_siriussuit', 'pthread_num',
                                  'dataset_size'),
                'result_fields': ('result_run_time', ),
                'best_result': 'min',
                'result_alias_fields': ('reference_link', 'result_passed',
                                        'result_warnings', 'result_errors',
                                        'cpu_type'),
                }
        self.app_infor['sparkterasort'] = {
                'information_module': st_i,
                'machine_module': st_m,
                'multi_child_app': (False, ''),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('data_size', 'processor_number',
                                  'partition_size', 'workers', 'bench_type',
                                  'smt', 'cores', 'executor_memory' ),
                'result_fields': ('result_time', ),
                'best_result': 'min',
                'result_alias_fields': ('data_size', 'partition_size',
                                        'workers', 'processor_number',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['speccpu'] = {
                'information_module': scpu_i,
                'machine_module': scpu_m,
                'multi_child_app': (False, ''),
                'machine_fields': ('half_l3_speccpu', 'existing_l4_speccpu'),
                'range_fields': None,
                'choice_fields': ('copies', ),
                # TODO: more than one result fields.
                'result_fields': ('result_int_rate_ratio',
                                  'result_fp_rate_ratio', ),
                'best_result': 'max',
                'result_alias_fields': ('copies', 'reference_link',
                                        'cpu_type'),
                }
        self.app_infor['specjbb'] = {
                'information_module': sjbb_i,
                'machine_module': sjbb_m,
                'multi_child_app': (True, 'app_name_specjbb'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('jvm_parameter_specjbb', 'jvm_instances',
                                  'warehouses'),
                'result_fields': ('result_bops', ),
                'best_result': 'max',
                'result_alias_fields': ('jvm_parameter_specjbb',
                                        'jvm_instances', 'warehouses',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['specjvm'] = {
                'information_module': sjvm_i,
                'machine_module': sjvm_m,
                'multi_child_app': (True, 'app_name_specjvm'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('app_name_specjvm', 'jvm_parameter_specjvm',
                                  'specjvm_parameter'),
                'result_fields': ('result_bops', ),
                'best_result': 'max',
                'result_alias_fields': ('jvm_parameter_specjvm', 'cpu_type',
                                        'specjvm_parameter', 'reference_link'),
                }
        self.app_infor['splash'] = {
                'information_module': spl_i,
                'machine_module': spl_m,
                'multi_child_app': (True, 'app_name_splash'),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('problem_size', 'app_name_splash'),
                'result_fields': ('result_time', ),
                'best_result': 'min',
                'result_alias_fields': ('problem_size', 'app_name_splash',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['tpcc'] = {
                'information_module': tpc_i,
                'machine_module': tpc_m,
                'multi_child_app': (False, ''),
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('warehouses', 'terminals'),
                'result_fields': ('result_tpmc', ),
                'best_result': 'max',
                'result_alias_fields': ('warehouses', 'terminals',
                                        'reference_link', 'cpu_type'),
                }
        self.app_infor['webserving'] = {
                'information_module': ws_i,
                'machine_module': ws_m,
                'multi_child_app': (False, ''),
                # machine_fields only fits for application who owns one machine
                'machine_fields': None,
                'range_fields': None,
                'choice_fields': ('warm_up', 'con_users', 'pm_static',
                                  'pm_max_connections', 'sql_max_connections',
                                  'network_bandwidth_webserving'),
                'result_fields': ('result_ops', ),
                'best_result': 'max',
                'result_alias_fields': ('reference_link', 'result_passed',
                                        'result_warnings', 'result_errors',
                                        'warm_up', 'con_users', 'pm_static',
                                        'pm_max_connections',
                                        'sql_max_connections',
                                        'worker_processes',
                                        'worker_connection',
                                        'network_bandwidth_webserving',
                                        'cpu_type'),
                }


class SearchIndexView(generic.TemplateView):
    """
    This view is inherited from generic.TemplateView and achieve:
    1.get base information related to all applications from models system;
    2.get all search input items and corresponding data which is from db;
    """
    template_name = 'performance/search/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchIndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SearchIndexView, self).get_context_data(**kwargs)

        # get all applications base information from configuration
        apps_base_infors_object = ApplicationBaseInformation()
        applications = apps_base_infors_object.applications
        apps_base_infors = apps_base_infors_object.app_infor

        app_infors_base = {}
        for app in applications:
            app_infors_base[app] = self.get_models_information(
                    apps_base_infors[app]['information_module'],
                    apps_base_infors[app]['range_fields'],
                    apps_base_infors[app]['choice_fields'],
                    )
        app_infors_webserving_base = app_infors_base['webserving']
        app_infors_webserving_extra = self.get_webserving_information()
        app_infors_base['webserving'] = dict(app_infors_webserving_base,
                                             **app_infors_webserving_extra)

        app_infors_mach = {}
        for app in applications:
            app_infors_mach[app] = self.get_models_information(
                    apps_base_infors[app]['machine_module'],
                    choice_field_list=apps_base_infors[app]['machine_fields']
                    )

        app_infors = {}
        for app in applications:
            if len(app_infors_mach) == 0:
                app_infors[app] = app_infors_base[app]
            else:
                app_infors[app] = dict(app_infors_base[app],
                                       **app_infors_mach[app])

        # render the context to template system
        ctx['project_names'] = project_names
        # ctx['architectures'] = architectures
        ctx['cpu_types'] = cpu_types
        ctx['applications'] = applications
        ctx['app_infors'] = app_infors
        return ctx

    def get_webserving_information(self):
        """
        add more 3 webserving filter condition:
        1. frontend_half_l3 = machine_side==frontend && half_l3
        2. backend_half_l3 = machine_side==backend && half_l3
        3. concurrent_connections = (worker_connection, worker_processes)
        """
        app_data = {}
        all_webserving_records = [i for i in ws_i.objects.all()]
        worker_connection_options = [i.worker_connection for i in
                                     all_webserving_records]
        worker_processes = [i.worker_processes for i in
                            all_webserving_records]
        app_data['concurrent_connections'] = list({(x, y) for x in
                worker_connection_options for y in worker_processes})
        app_data['frontend_half_l3'] = [True, False]
        app_data['backend_half_l3'] = [True, False]
        return app_data

    def get_limit_value(self, module_info, field_name):
        field_value_list = [i.__getattribute__(field_name) for i in
                            module_info]
        return (min(field_value_list), max(field_value_list))

    def get_all_value(self, module_info, field_name):
        field_value_list = list(set([i.__getattribute__(field_name) for i in
                                     module_info]))
        return sorted(field_value_list)

    def get_gaps_value_list(self, min_one, max_one, segment_number=5):
        value_range = max_one - min_one
        if value_range <= (segment_number * 2):
            return [(min_one, max_one)]
        # gaps_value = value_range // segment_number
        gaps_value = value_range / segment_number
        # gaps_list = [min_one + gaps_value * i if i < segment_number else
        #        max_one for i in range(segment_number+1)]
        gaps_list = []
        previous_one = min_one
        for i in range(1, segment_number):
            if i % 2 == 1:
                next_one = math.floor(min_one + i * gaps_value)
            else:
                next_one = math.ceil(min_one + i * gaps_value)
            gaps_list.append((previous_one, next_one))
            previous_one = 1 + next_one
        gaps_list.append((previous_one, max_one))
        return gaps_list

    def get_models_information(self, module_name, range_field_list=None,
                               choice_field_list=None):
        """
        get the value range by looking for the value of field_name 
        in the module. such as: 
        app_data['data_scale'] = [(10, 20), (21, 30), (31, 40)]
        app_data['network_bandwidth_datacaching'] = [1000, 2000, 4000, 
                5000, 8000,10000]
        """
        app_data = {}
        if module_name.objects.exists():
            module_info = [i for i in module_name.objects.all()]
        else:
            print("Still no data in {0}".format(module_name))
            if range_field_list:
                for field_name in range_field_list:
                    app_data[field_name] = [(0, 0)]
            if choice_field_list:
                for field_name in choice_field_list:
                    app_data[field_name] = ["no data"]
            return app_data
        if range_field_list is not None:
            for field_name in range_field_list:
                min_field_value, max_field_value = self.get_limit_value(
                        module_info, field_name)
                app_data[field_name] = self.get_gaps_value_list(
                        min_field_value, max_field_value)
        if choice_field_list is not None:
            for field_name in choice_field_list:
                app_data[field_name] = self.get_all_value(module_info,
                                                          field_name)
        return app_data


class SearchResultView(generic.TemplateView):
    """
    1. Get the post options and search data from db.
    2. show filtered data into table or figure
    """
    # template_name = 'performance/search/result.html'

    def __init__(self, **kwargs):
        super(SearchResultView, self).__init__(**kwargs)
        # get all applications base information from configuration
        self.apps_base_infors_object = ApplicationBaseInformation()
        self.applications = self.apps_base_infors_object.applications
        self.apps_base_infors = self.apps_base_infors_object.app_infor
        # The template_name should be determined by user submission
        self.template_name = 'performance/search/result_error.html'

    def get_same_element_in_list(self, list_former, list_latter):
        return list(set(list_former).intersection(list_latter))

    def get_all_field_name(self, module_name, exclude_list=()):
        field_name_list = [field.name for field in module_name._meta.fields
                           if field.name not in exclude_list]
        return field_name_list

    def get_all_field_verbose_name(self, module_name, exclude_list=()):
        """
        Still use field.name in exclude_list because field.name is stored
        in db which is more stable.
        """
        field_verbose_name_list = [field.verbose_name for field in
                                   module_name._meta.fields if field.name not
                                   in exclude_list]
        return field_verbose_name_list

    def convert_string_to_tuple(self, string_name):
        trans_map = str.maketrans('(),', '   ')
        string_list = string_name.translate(trans_map).strip().split()
        min_one = float(string_list[0])
        max_one = float(string_list[1])
        return (min_one, max_one)

    def judge_webserving_machine(self, every_group, frontend_half_l3,
                                 # fronend_arch, backend_half_l3):
                                 backend_half_l3):
        # init_dict = {'frontend': (None, None), 'backend': None}
        init_dict = {'frontend': None, 'backend': None}
        for record in every_group:
            machine_side = record.machine_side
            half_l3 = record.half_l3
            # arch = record.architecture_type
            if machine_side == 'frontend':
                if frontend_half_l3 == "all_options":
                    # init_dict['frontend'] = (frontend_half_l3, arch)
                    init_dict['frontend'] = frontend_half_l3
                else:
                    # init_dict['frontend'] = (half_l3, arch)
                    init_dict['frontend'] = half_l3
            elif machine_side == 'backend':
                if backend_half_l3 == "all_options":
                    init_dict['backend'] = backend_half_l3
                else:
                    init_dict['backend'] = half_l3
        # if init_dict['frontend'] == (frontend_half_l3, fronend_arch) \
        if init_dict['frontend'] == frontend_half_l3 \
                and init_dict['backend'] == backend_half_l3:
            return True
        else:
            return False

    def filter_needed_id(self, module_info, field_value_map, flag,
                         filter_field='id'):
        record_id_list = []
        for record_info in module_info:
            record_id = record_info.__getattribute__(filter_field)
            record_id_flag = True
            for field_name, field_value in field_value_map.items():
                record_field_value = record_info.__getattribute__(field_name)
                if flag == "choice":
                    if record_field_value != field_value:
                        # This record should be satisified with all options
                        record_id_flag = False
                        break
                elif flag == "range":
                    if (record_field_value < field_value[0]) or (
                            record_field_value > field_value[1]):
                        record_id_flag = False
                        break
            if record_id_flag:
                record_id_list.append(record_id)
        return record_id_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchResultView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SearchResultView, self).get_context_data(**kwargs)
        ctx['kwargs'] = kwargs
        return ctx

    def post(self, request, *args, **kwargs):
        # the context being rendered store into kwargs
        kwargs = {}
        all_post_data = request.POST

        # base search items
        post_display_form = all_post_data.get('display_as')
        post_project_name = all_post_data.get('project_names')
        post_begin_time = all_post_data.get('begin_time')
        post_end_time = all_post_data.get('end_time')
        post_cpu_type = all_post_data.get('cpu_types')
        # post_architecture = all_post_data.get('architectures')
        post_application = all_post_data.get('applications')

        # further search items related to application name
        post_app_i_module = self.apps_base_infors[
                post_application]['information_module']
        post_app_m_module = self.apps_base_infors[
                post_application]['machine_module']
        post_app_range_field_list = self.apps_base_infors[post_application][
                'range_fields']
        post_app_choice_field_list = self.apps_base_infors[post_application][
                'choice_fields']
        post_app_machine_field_list = self.apps_base_infors[post_application][
                'machine_fields']
        child_app_attr, child_app_name = self.apps_base_infors[
                post_application]['multi_child_app']
        post_best_result = self.apps_base_infors[post_application][
                'best_result']

        # get all chosen options of user and extract filter condition - start
        base_search_item_value_map = {}
        further_search_item_value_map = {}
        base_search_item_value_map['project_name'] = post_project_name
        base_search_item_value_map['cpu_type'] = post_cpu_type
        # base_search_item_value_map['architecture'] = post_architecture
        base_search_item_value_map['application'] = post_application
        base_search_item_value_map['begin_time'] = post_begin_time
        base_search_item_value_map['end_time'] = post_end_time
        post_begin_time_format = datetime.datetime.strptime(
                post_begin_time, '%Y-%m-%d %H:%M:%S')
        post_end_time_format = datetime.datetime.strptime(
                post_end_time, '%Y-%m-%d %H:%M:%S')

        # get needed record from XXXInformation module
        i_filter_kwargs = {}
        i_filter_kwargs['project_name__exact'] = post_project_name
        if post_cpu_type != "all_options":
            i_filter_kwargs['cpu_type__exact'] = post_cpu_type
        i_filter_kwargs['record_result_time__range'] = (post_begin_time_format,
                                                        post_end_time_format)
        graph_x_field_list = []
        if post_app_range_field_list is not None:
            for i in post_app_range_field_list:
                field_value = all_post_data.get(i)
                if field_value != "all_options":
                    field_value = self.convert_string_to_tuple(
                            all_post_data.get(i))
                    i_filter_kwargs['{0}__{1}'.format(i, "range")] = \
                        field_value
                    further_search_item_value_map[i] = field_value
                else:
                    further_search_item_value_map[i] = "ALL"
                    graph_x_field_list.append(i)
        if post_app_choice_field_list is not None:
            for i in post_app_choice_field_list:
                field_value = all_post_data.get(i)
                if field_value != "all_options":
                    # FIXME: store value is a bool type but
                    # get string when get from user input
                    if field_value == "False":
                        field_value = False
                    elif field_value == "True":
                        field_value = True
                    i_filter_kwargs['{0}__{1}'.format(i, "exact")] = \
                        field_value
                    further_search_item_value_map[i] = field_value
                else:
                    further_search_item_value_map[i] = "ALL"
                    graph_x_field_list.append(i)

        if post_app_machine_field_list is not None:
            for i in post_app_machine_field_list:
                field_value = all_post_data.get(i)

        if post_application == 'webserving':
            concurrent_connections_temp = all_post_data.get(
                    'concurrent_connections')
            if concurrent_connections_temp != "all_options":
                concurrent_connections_value = self.convert_string_to_tuple(
                    concurrent_connections_temp)
                worker_connection = concurrent_connections_value[0]
                worker_processes = concurrent_connections_value[1]
                i_filter_kwargs['worker_connection__exact'] = \
                    worker_connection
                i_filter_kwargs['worker_processes__exact'] = \
                    worker_processes
                further_search_item_value_map['concurrent_connections'] = \
                    concurrent_connections_value
            else:
                further_search_item_value_map['concurrent_connections'] = \
                    "ALL"
                graph_x_field_list.append('concurrent_connections')

        i_module_needed_queryset = post_app_i_module.objects.filter(
                **i_filter_kwargs)
        i_id_list = [record.id for record in i_module_needed_queryset]

        # get needed record from XXXMachine module
        m_filter_kwargs = {}
        if post_application == 'webserving':
            # XXX: must convert string to bool here for frontend/backend
            frontend_half_l3_temp = all_post_data.get('frontend_half_l3')
            backend_half_l3_temp = all_post_data.get('backend_half_l3')
            if frontend_half_l3_temp != "all_options":
                further_search_item_value_map['frontend_half_l3'] = \
                        frontend_half_l3_temp
                frontend_half_l3 = True if frontend_half_l3_temp == 'True' \
                    else False
            else:
                frontend_half_l3 = frontend_half_l3_temp
                further_search_item_value_map['frontend_half_l3'] = \
                    "ALL"
                graph_x_field_list.append('frontend_half_l3')
            if backend_half_l3_temp != "all_options":
                further_search_item_value_map['backend_half_l3'] = \
                        backend_half_l3_temp
                backend_half_l3 = True if backend_half_l3_temp == 'True' \
                    else False
            else:
                backend_half_l3 = backend_half_l3_temp
                further_search_item_value_map['backend_half_l3'] = \
                    "ALL"
                graph_x_field_list.append('backend_half_l3')
            ws_m_id_list = {i.app_information_id for i in ws_m.objects.all()}
            m_id_list = []
            for id_value in ws_m_id_list:
                every_group = [i for i in ws_m.objects.filter(
                        app_information_id__exact=id_value)]
                if self.judge_webserving_machine(every_group, frontend_half_l3,
                                                 backend_half_l3):
                    m_id_list.append(id_value)
        else:
            # m_filter_kwargs['architecture_type__exact'] = post_architecture
            if post_app_machine_field_list is not None:
                for i in post_app_machine_field_list:
                    field_value = all_post_data.get(i)
                    if field_value != "all_options":
                        if field_value == "False":
                            field_value = False
                        elif field_value == "True":
                            field_value = True
                        m_filter_kwargs['{0}__{1}'.format(i, "exact")] = \
                            field_value
                        further_search_item_value_map[i] = field_value
                    else:
                        further_search_item_value_map[i] = "ALL"
                        graph_x_field_list.append(i)
            m_module_needed_queryset = post_app_m_module.objects.filter(
                    **m_filter_kwargs)
            m_id_list = [record.app_information_id for record in
                         m_module_needed_queryset]
        # merge same value because ForeignKey in .models
        id_list = self.get_same_element_in_list(i_id_list, m_id_list)
        # get all chosen options of user and extract filter condition - end
        # From here: all display form are based on the id_list filter from
        # user's input

        # public kwargs
        kwargs['base_search_item_value_map'] = base_search_item_value_map
        kwargs['further_search_item_value_map'] = further_search_item_value_map

        if post_display_form == "graph":
            if len(graph_x_field_list) != 1:
                self.template_name = 'performance/search/result_error.html'
                kwargs['graph_error_message'] = "If you show it as 'Graph', only one choices can be 'all options'."
            else:
                self.template_name = 'performance/search/result_graph.html'
                result_fields = self.apps_base_infors[
                        post_application]['result_fields']
                result_alias_fields = self.apps_base_infors[
                        post_application]['result_alias_fields']
                graph_x_field = graph_x_field_list[0]
                graph_y_field = result_fields[0]
                figure_needed_record_list = [record for record in
                                             i_module_needed_queryset.order_by(
                                                 graph_x_field)
                                             if record.id in id_list]
                result_fields_value_list = []
                for record in figure_needed_record_list:
                    result_x_value = record.__getattribute__(graph_x_field)
                    result_y_value = record.__getattribute__(graph_y_field)
                    result_fields_value_list.append([
                        result_x_value, result_y_value,
                        {i: record.__getattribute__(i) for i
                            in result_alias_fields},])
                # If same x value has several y values, delete all of them but
                # remain only one and replace its y value by theirs average value.
                i = 0
                while i < len(result_fields_value_list):
                    j = i + 1
                    count = 1
                    sum = result_fields_value_list[i][1]
                    while j < len(result_fields_value_list) and result_fields_value_list[i][0] == result_fields_value_list[j][0]:
                        count += 1
                        sum += result_fields_value_list[j][1]
                        j += 1

                    if count > 1:
                        result_fields_value_list[i][1] = sum/count
                        result_fields_value_list[i][2]["Tips"] = "Average value of {0} points".format(count)
                        k = 1
                        while k < count:
                            result_fields_value_list.pop(i + 1)
                            k += 1
                        i = j
                    else:
                        i += 1

                kwargs['graph_x_field'] = graph_x_field
                kwargs['graph_y_field'] = graph_y_field
                kwargs['result_fields_value_list'] = result_fields_value_list
        elif post_display_form == "figure":
            # FIXME: should be get all result fields.
            result_fields = self.apps_base_infors[
                    post_application]['result_fields']
            result_alias_fields = self.apps_base_infors[
                    post_application]['result_alias_fields']
            figure_needed_record_list = [record for record in
                                         i_module_needed_queryset.order_by(
                                             'record_result_time')
                                         if record.id in id_list]
            if post_cpu_type == 'all_options':
                self.template_name = 'performance/search/result_all_cpu_type.html'
                result_fields_map = collections.OrderedDict()
                cpu_type_set = tuple({i.cpu_type for i in
                                      figure_needed_record_list})
                if child_app_attr:
                    app_name_set = tuple({i.__getattribute__(child_app_name)
                                          for i in figure_needed_record_list})
                    """eg: {
                        cpu1: [(max_value_app1, 'Hello'), (max_value_app2, 'Hello')], 
                        cpu2: [(max_value_app1, 'Hello'), (max_value_app2, 'Hello')]
                        }
                    """
                    result_fields_map = collections.OrderedDict({i: [] for i in
                                                                 cpu_type_set})
                    for app, cpu in itertools.product(app_name_set,
                                                      cpu_type_set):
                        temp = []
                        found = False
                        for index, record in enumerate(figure_needed_record_list):
                            if record.cpu_type == cpu and record.__getattribute__(
                                    child_app_name) == app:
                                found = True
                                temp.append((index,record.__getattribute__(
                                        result_fields[0])))
                        if not found:
                            max_value = 0
                            alias_field_map = {}
                        else:
                            max_value = temp[0][1]
                            max_index = temp[0][0]
                            if post_best_result == 'max':
                                for ii in temp:
                                    if ii[1] > max_value:
                                        max_index = ii[0]
                                        max_value = ii[1]
                            elif post_best_result == 'min':
                                for ii in temp:
                                    if ii[1] < max_value:
                                        max_index = ii[0]
                                        max_value = ii[1]
                            max_record = figure_needed_record_list[max_index]
                            alias_field_map = {i: max_record.__getattribute__(i)
                                               for i in result_alias_fields}
                        result_fields_map[cpu].append((max_value, alias_field_map))
                else:
                    app_name_set = ('Default', )
                    for cpu in cpu_type_set:
                        temp = []
                        for index, record in enumerate(figure_needed_record_list):
                            if record.cpu_type == cpu:
                                temp.append((index,record.__getattribute__(
                                        result_fields[0])))
                        max_value = temp[0][1]
                        max_index = temp[0][0]
                        if post_best_result == 'max':
                            for ii in temp:
                                if ii[1] > max_value:
                                    max_index = ii[0]
                                    max_value = ii[1]
                        elif post_best_result == 'min':
                            for ii in temp:
                                if ii[1] < max_value:
                                    max_index = ii[0]
                                    max_value = ii[1]
                        max_record = figure_needed_record_list[max_index]
                        alias_field_map = {i: max_record.__getattribute__(i)
                                           for i in result_alias_fields}
                        result_fields_map[cpu] = [(max_value, alias_field_map)]
                kwargs['graph_y_field'] = result_fields[0]
                kwargs['app_name_set'] = app_name_set
                kwargs['result_fields_map'] = result_fields_map
            else:
                self.template_name = 'performance/search/result_figure.html'
                result_fields_value_list = []
                for record in figure_needed_record_list:
                    result_x_value = 1000 * int(
                            record.record_result_time.strftime('%s'))
                    result_y_value = record.__getattribute__(result_fields[0])
                    result_fields_value_list.append((
                            result_x_value, {result_fields[0]: result_y_value},
                            {i: record.__getattribute__(i) for i
                                in result_alias_fields},))
                result_fields_map = {j: [] for j in {i[2]['cpu_type'] for i in
                                     result_fields_value_list}}
                for i in result_fields_value_list:
                    record_cpu_type = i[2]['cpu_type']
                    result_fields_map[record_cpu_type].append(i)
                kwargs['result_fields_map'] = result_fields_map
        elif post_display_form == "table":
            self.template_name = 'performance/search/result_table.html'
            i_field_name_list = self.get_all_field_name(post_app_i_module,
                    exclude_list=('test_application', 'record_result_time', ))
            m_field_name_list = self.get_all_field_name(post_app_m_module,
                    exclude_list=('dependence_information', 'last_modify_time',
                                  'app_information'))
            i_field_verbose_name_list = self.get_all_field_verbose_name(
                    post_app_i_module, exclude_list=('test_application',
                                                     'record_result_time', ))
            m_field_verbose_name_list = self.get_all_field_verbose_name(
                    post_app_m_module, exclude_list=('dependence_information',
                                                     'last_modify_time',
                                                     'app_information'))
            record_value_list = []
            # when display as table, use id of i_module as keyword
            for id_value in sorted(id_list):
                i_record_list = [i for i in post_app_i_module.objects.filter(
                    id__exact=id_value)]
                m_record_list = [i for i in post_app_m_module.objects.filter(
                    app_information_id__exact=id_value)]
                i_record_value = [i_record_list[0].__getattribute__(field_name)
                                  for field_name in i_field_name_list]
                # len(i_record_list) always == 1, but len(m_record_list) >= 1
                every_record_value = copy.deepcopy(i_record_value)
                every_record_value.append('    ')
                for m_record in m_record_list:
                    # if m_record.machine_side not in ('server_side',
                    #        'frontend'):
                    #    continue
                    # FIXME:break i_module_info and m_module_info into two parts
                    for field_name in m_field_name_list:
                        every_record_value.append(m_record.__getattribute__(
                            field_name))
                record_value_list.append(every_record_value)
            # kwargs['i_module_header'] = i_field_name_list
            # kwargs['m_module_header'] = m_field_name_list
            kwargs['i_module_header'] = i_field_verbose_name_list
            if post_application == 'webserving':
                kwargs['m_module_header'] = m_field_verbose_name_list * 3
            elif post_application in ('datacaching', 'tpcc'):
                kwargs['m_module_header'] = m_field_verbose_name_list * 2
            else:
                kwargs['m_module_header'] = m_field_verbose_name_list
            kwargs['record_value_list'] = record_value_list
        elif post_display_form == "report":
            self.template_name = 'performance/search/report_output.html'
            filename = '{0}_test_report.pdf'.format(post_application)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
            lst = []
            # -------- all needed original data from here -------------#
            # logo_data = 'POWERCORE http://www.powercore.com.cn'
            report_title_data = 'The Test Report On Application of {0}'.format(
                    post_application)
            main_table_title_data = 'Table 1: The Test Environment of {0}'.format(post_application)
            main_table_data = []
            mtd_header = ('CPU\nType', 'Role', 'Machine\nName', 'Architecture',
                    'CPU Clock\nRate(GHZ)', 'L2 Cache\n(KB)', 'L3 Cache\n(KB)',
                    'Operation\nSystem', 'Kernel\nVersion', 'Endian\nMode')
            mtd_list = ('machine_side', 'machine_name', 'architecture_type',
                    'cpu_frequency', 'l2', 'l3', 'os_type', 'kernel_version',
                    'byte_order')
            main_table_data.append(mtd_header)
            mtd_index_list = []
            index = 0
            # get random record has different cpu_type
            cpu_id_map = {i[1]: i[0] for i in post_app_i_module.objects.
                          values_list('id','cpu_type').distinct()}
            id_cpu_map = {j:i for i, j in cpu_id_map.items()}
            main_table_id_list = [i for i in cpu_id_map.values()]
            for id_value in main_table_id_list:
                mtd_cpu_type = id_cpu_map[id_value]
                mtd_records = [i for i in post_app_m_module.objects.filter(
                    app_information_id__exact=id_value)]
                first_time = True
                for record in mtd_records:
                    tmp = []
                    index += 1
                    if first_time:
                        tmp.append(mtd_cpu_type)
                        start = index
                        first_time = False
                    else:
                        tmp.append(None)
                    for i in mtd_list:
                        field_value = record.__getattribute__(i)
                        if i == 'machine_side':
                            tmp.append(field_value.replace('_side', ''))
                        elif i == 'byte_order':
                            tmp.append(field_value.replace('_endian', ''))
                        else:
                            tmp.append(field_value)
                    main_table_data.append(tmp)
                if start < index:
                    mtd_index_list.append((start, index))  # here: stop = index

            conf_table_title_data = 'Table 2: The Configurations of {0}'.format(
                    post_application)
            conf_table_data = []
            # child_app_attr, child_app_name
            # content_in_conf_table_data  -- begin
            result_fields = self.apps_base_infors[
                    post_application]['result_fields']
            result_alias_fields_bak = self.apps_base_infors[
                    post_application]['result_alias_fields']
            result_alias_fields = []
            for i in result_alias_fields_bak:
                if i == 'reference_link' or i == 'cpu_type' \
                    or 'app_name_' in i:
                    continue
                else:
                    result_alias_fields.append(i)
            result_alias_fields_len = len(result_alias_fields)
            needed_records = [i for i in i_module_needed_queryset.order_by(
                              'record_result_time') if i.id in id_list]
            conf_maps = {}
            cpu_type_set = tuple({i.cpu_type for i in needed_records})
            if child_app_attr:
                app_name_set = tuple({i.__getattribute__(child_app_name)
                                      for i in needed_records})
                for app, cpu in itertools.product(app_name_set, cpu_type_set):
                    conf_maps[(app, cpu)] = []
            else:
                for cpu in cpu_type_set:
                    conf_maps[('Default', cpu)] = []
            for record in needed_records:
                result_list = []
                conf_cpu_type = record.cpu_type
                if child_app_attr:
                    conf_app_name = record.__getattribute__(child_app_name)
                else:
                    conf_app_name = 'Default'
                conf_result = record.__getattribute__(result_fields[0])
                result_list.append(conf_result)
                conf_values = [record.__getattribute__(i) for i in
                               result_alias_fields]
                result_list += conf_values
                conf_maps[(conf_app_name, conf_cpu_type)].append(result_list)
            conf_table_data = []
            cpu_type_col_name = 'CPU Type'
            if child_app_attr:
                app_name_col_name = 'App Names'
            else:
                app_name_col_name = 'Default App Name'
            first_col = [app_name_col_name, cpu_type_col_name]
            for i in result_alias_fields:
                first_col.append(i)
            conf_table_data.append(first_col)
            main_figure_maps = {}
            for app_cpu, result_list in conf_maps.items():
                col_values = [app_cpu[0], app_cpu[1]]
                if not result_list:
                    col_values += ['-' for _ in range(result_alias_fields_len)]
                    conf_table_data.append(col_values)
                    main_figure_maps[app_cpu] = 0
                    continue
                best_result = result_list[0]
                for i in result_list:
                    if post_best_result == 'max' and i[0] > best_result[0]:
                        best_result = i
                    elif post_best_result == 'min' and i[0] < best_result[0]:
                        best_result = i
                main_figure_maps[app_cpu] = best_result[0]
                col_values += best_result[1:]
                conf_table_data.append(col_values)
            if child_app_attr:
                conf_table_data_sorted = sorted(conf_table_data,
                                                key=lambda x:x[0])
            else:
                conf_table_data_sorted = sorted(conf_table_data,
                                        key=lambda x:x[1] != cpu_type_col_name)
            # Transpose the conf_table_data
            conf_table_data_trans = []
            col_width = len(conf_table_data_sorted[0])
            for i in range(col_width):
                conf_table_data_trans.append([x[i] for x in
                    conf_table_data_sorted])
            ctd_index_list = []
            if child_app_attr:
                # Can NOT use app_name_set to replace app_name_set_order here
                app_name_set_order = []
                for i in conf_table_data_trans[0][1:]:
                    if i not in app_name_set_order:
                        app_name_set_order.append(i)
                for i in app_name_set_order:
                    start = conf_table_data_trans[0].index(i)
                    num = conf_table_data_trans[0].count(i)
                    stop = start + num - 1
                    ctd_index_list.append((start, stop))
            else:
                # remove first_col for the application without app_name
                conf_table_data_trans = conf_table_data_trans[1:]

            main_figure_title_data = 'Figure 1: Best Result in Different App Names and CPU Types'
            main_figure_data = []
            y_max = int(max(main_figure_maps.values()) * 1.5)
            if child_app_attr:
                x_category = app_name_set
            else:
                x_category = ['Default']
            for cpu in cpu_type_set:
                tmp = []
                for app in x_category:
                    tmp.append(main_figure_maps[(app, cpu)])
                main_figure_data.append(tmp)

            space_05 = insert_space()
            # logo = show_content(logo_data, h1_style)
            logo_image_path = os.path.join('./performance/static/performance/img/',
                    'image_powercore.png')
            print('path is ', os.getcwd())
            # logo_image = insert_image(logo_image_path, 370, 72)
            # pls use command to get image's size: file image_filename
            logo_image = insert_image(logo_image_path, 208, 47)
            report_title = show_content(report_title_data, h2_style)
            main_table_title = show_content(main_table_title_data, h4_style)
            main_table = show_main_table(main_table_data, mtd_index_list)
            conf_table_title = show_content(conf_table_title_data, h4_style)
            conf_table = show_conf_table(conf_table_data_trans, ctd_index_list)
            main_figure_title = show_content(main_figure_title_data, h4_style)
            main_figure = show_figure(main_figure_data, y_max, x_category,
                                      cpu_type_set)

            # lst.append(logo)
            lst.append(logo_image)
            lst.append(space_05)
            lst.append(report_title)
            lst.append(space_05)
            lst.append(main_table_title)
            lst.append(main_table)
            lst.append(space_05)
            lst.append(conf_table_title)
            lst.append(conf_table)
            lst.append(space_05)
            lst.append(main_figure_title)
            lst.append(main_figure)

            SimpleDocTemplate(response, showBoundary=0, leftMargin=10,
                              rightMargin=10, topMargin=10, buttomMargin=10
                              ).build(lst)
            return response
        else:
            self.template_name = 'performance/search/result_error.html'

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

