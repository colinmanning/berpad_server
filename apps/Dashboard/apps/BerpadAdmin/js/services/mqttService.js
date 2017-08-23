backoffice.factory( 'mqttService', ['$rootScope', '$q', function ($rootScope, $q) {

    var factory = {};

    var client = null;
    var clientName = null;
    var connected = false;
    var username = null;

    var connections = {}

    factory.connect = function(client_name, broker_address, on_message, on_connection_lost, on_connect) {
        var cname = client_name;
        if (cname.length > 23) cname = cname.substring(0,23);
        if (connections[cname]) {
            return connections[cname];
        }
        try {
            connections[cname] = client;
            client = new Messaging.Client(broker_address, parseFloat(8088), cname);
            client.onMessageArrived = on_message;
            client.onConnectionLost = on_connection_lost;

            var seSsl = broker_address.startsWith("wss");

            var connectOptions = new Object();
            connectOptions.hosts = [ "wss://"+broker_address+":8000/" ];
            //connectOptions.hosts = [ broker_address+":8000/" ];
            //connectOptions.useSSL = useSsl;
            connectOptions.useSSL = true;
            connectOptions.cleanSession = true;
            connectOptions.userName = 'dashboard-user';
            connectOptions.password = 'lillymarie';
            connectOptions.keepAliveInterval = 3600;
            connectOptions.onSuccess = function (responseObject) {
                on_connect(responseObject, client);
            };
            connectOptions.onFailure = function (err) {
                console.log('err', err);
                delete connections[cname];
            };
            client.connect(connectOptions);
        }
        catch(err) {
            console.log('try error', err);
            return undefined;
        }

        return connections[cname];

    };

    function onConnectionLost(responseObject) {
        console.log("Connection Lost");
        //$rootScope.console += " | Connection Lost";
        client = null;
        $rootScope.$broadcast(factory.EVENT_CONNECTION_LOST);
    }

    function onConnection(responseObject) {
        console.log("Connection Established");
        //$rootScope.console += " | Connection Established";
        topic_sstream = "RK/SSTREAM/" + gateway_id + "/#";
        client.subscribe(topic_sstream);
        topic_config = "RK/ENOCEAN/CONFIG/" + gateway_id;
        client.subscribe(topic_config);
        setFastMode(FASTMODE_SECONDS);
    }

    function onMessageArrived(message) {
        var topic = message.destinationName;
        topic_bits = topic.split("/")
        switch (topic_bits[1]) {
            case TOPIC_TYPE_COMMAND:
                // not needed any more
                
                /*
                var devices = processDevices(JSON.parse(message.payloadString).devices);
                //var str = String.fromCharCode.apply(null, message.payloadBytes);
                //console.log("myMessage",str+ " or " + message.payloadString);
                //console.log(message);
                $rootScope.$broadcast(factory.EVENT_GATEWAY_DEVICES_RETURNED, devices);
                */
                break;
            default:
                break
        }
    }


    factory.setGateway = function(id, mqttBroker) {
        return $q(function(resolve, reject) {
            try {
                if (mqttBroker == null || mqttBroker == '') {
                    mqttBroker = DEFAULT_MQTT_BROKER;
                }
                if (!client) {
                    clientName = "rk_ttool_p_" + $rootScope.username + $rootScope.myIP;
                    if (clientName.length > 23) clientName = clientName.substring(0,23);

                    client = new Messaging.Client(mqttBroker, parseFloat(8088), clientName);
                    client.onMessageArrived = onMessageArrived;
                    client.onConnectionLost = onConnectionLost;
                    gateway_id = id;
                    console.log("gateway_id", gateway_id);
                    //$rootScope.console += " | gateway_id: " + gateway_id;
                    //$rootScope.console += " | wss://"+mqttBroker+":8000/";
                    var connectOptions = new Object();
                    connectOptions.hosts = [ "wss://"+mqttBroker+":8000/" ];
                    connectOptions.useSSL = true;
                    connectOptions.cleanSession = true;
                    connectOptions.userName = 'dashboard-user';
                    connectOptions.password = 'lillymarie';
                    connectOptions.keepAliveInterval = 3600;
                    connectOptions.onSuccess = function (responseObject) {
                        onConnection(responseObject);
                    };
                    connectOptions.onFailure = function (err) {
                        console.log('err',err);
                        //$rootScope.console += " | error: "+err.errorCode + " " +err.errorMessage;
                        reject();
                    };
                    client.connect(connectOptions);
                } else {
                    // TODO we need to tidy up, unsubscribe etc
                    client.unsubscribe(topic_config);
                    client.unsubscribe(topic_sstream);
                    onConnection();
                } 
            } catch (err) {
                reject(err)
            }
        });
    }

    factory.getGatewayDevices = function() {

        var command = {'command': 'GET ENOCEANCONFIG'};
        var message = new Messaging.Message(JSON.stringify(command));
        message.destinationName = "RK/COMMAND/" + gateway_id;
        client.send(message);
    }

    return factory;
}]);