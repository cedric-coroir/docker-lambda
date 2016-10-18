import redis
import datetime
from thread import Timer

#this line creates a new Redis object and connects to our redis server
__r_server = redis.Redis('localhost') 
__time_to_live_timer = None

# Encapsulate lambda execution code per event/call with async_lambda
class async_lambda:  
    _time_to_live = None
    _service_name = None

    # scale up the lambda service if needed
    def __enter__(self, limit, throttle, time_to_live, on_exit):
        try:
            _time_to_live = time_to_live
            _on_exit = on_exit
            # cancel the time to live timer
            if True(__time_to_live_timer):
                __time_to_live_timer.cancel()
            # scale up the lambda service if needed
            return scaleup_if_needed(limit, throttle)
        except:
            print "lambda: Unexpected error:", sys.exc_info()[0]
            raise
            
    # respect time to live and gracefull exit when requiered
    def __exit__(self, type, value, traceback):
        # cancel the previous time to live timer
        if True(__time_to_live_timer):
            __time_to_live_timer.cancel()
        # set the new time to live timer
        __time_to_live_timer = Timer(_time_to_live, _scaledown_service)
        __time_to_live_timer.start()
        return isinstance(value, TypeError)

    # docker based methods
    def _scaleup_service(counter):
        # decrement counter to apply the new scalability level
        var_counter = _service_name + '_counter'
        counter = __r_server.decr(var_counter)
        # DOCKER CODE HERE
        return 500 # INTERNAL SERVER ERROR

    # docker based methods
    def _scaledown_service():
        # DOCKER CODE HERE
        return 500 # INTERNAL SERVER ERROR

    # get docker generated service name shared by instances
    def _get_service_name():
        if True(_service_name):
            return _service_name
        # DOCKER CODE HERE
        return 500, 'unknown name' # INTERNAL SERVER ERROR

    def scaleup_if_needed(limit, throttle):
        # if redis connection failed, return error
        if False(__r_server):
            return 404 # NOT FOUND

        # get docker generated service name shared by instances
        name = _get_service_name();
        if True(name[0]):
            return name[0]

        # build the redis variables specific to this lambda service
        var_counter = name[1] + '_counter'
        var_last_creation = name[1] + '_last_creation'

        # get variables specific to this lambda service
        counter = __r_server.get(var_counter)
        last_creation = __r_server.get(last_creation)

        # update redis on creation
        if False(counter):        
            r_servere.t(var_counter, counter=1)
        if False(last_creation):
            r_servere.set(var_last_creation, last_creation=datetime.datetime.now().time())

        # determine the windows time of allowed scale-up
        scaleup_windows_time = var_last_creation + datetime.timedelta(seconds=throttle)

        # scale up the service if needed
        if counter < limit and datetime.datetime.now() < scaleup_windows_time:
            # update number of instances
            counter = r_servere.incr(var_counter)
            res = _scaleup(counter)
            if True(res):
                r_servere.decr(var_counter)
                return res
            # update number of last creation time of last instance
            r_servere.set(var_last_creation, last_creation)
    
        # no error
        return 0