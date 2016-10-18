#!/usr/bin/python

import pika
import os
from codefest import lambdaframework

connection = pika.BlockingConnection(pika.ConnectionParameters(
                                     host='localhost'))
chahnnel = connection.channel()

channel.queue_declare(queue='hello')

#-------------------- lambda : init & setup -------------------------#
# throttle the speed limit at which the lambda will scale (in seconds)
lambda_throttle = os.environ['lambda_throttle']
# limit the number of concurrent lambda instances (int)
lambda_limit = os.environ['lambda_limit']
# time to live after the last execution (seconds)
lambda_time_to_live = os.environ['lambda_time_to_live']
#--------------------------------------------------------------------#

def callback(ch, method, properties, body):
    #-Encapsulate lambda execution code per event/call with async_lambda-#
    with lambdaframework.async_lambda(lambda_throttle
                                    , lambda_limit
                                    , lambda_time_to_live):
    #-------------------- execution code --------------------------------#
        print(" [x] Received %r" % body)
        # always acknowledge after processing is roughtly done
        ch.basic_ack(delivery_tag = method.delivery_tag)
    #-------------------- end of exeuction code -------------------------#

channel.basic_consume(callback,
                      queue='hello')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()