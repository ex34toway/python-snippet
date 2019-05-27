# -*- coding:utf-8 -*-
import yaml

if __name__ == "__main__":
    document = """
    server:
        port: 8081
        tomcat:
            min-spare-threads: 5
            max-threads: 200
            uri-encoding: UTF-8
    """
    config = yaml.load(document)
    server = config['server']
    print(server['port'])
    print(server['tomcat']['min-spare-threads'])
    print(server['tomcat']['max-threads'])
    print(server['tomcat']['uri-encoding'])
    print(type(server))
