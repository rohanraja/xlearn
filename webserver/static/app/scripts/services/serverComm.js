angular.module("sbAdminApp").provider('serverComm', function(){

	this.commMethod = "http"; // For later config use. 

	var makeUrl = function(){

		return "/http_api";

	};

	var makeRequestPacket = function(query){
		
		_data = {
			'query': query
		}
		return $.param({data: angular.toJson(_data)});

	};

	this.$get = function($http, $q){
		return{	

			getData: function(query){

				var finalUrl = makeUrl();
				var request_packet = makeRequestPacket(query);

				var deferred = $q.defer();
				$http({
					method: 'POST',
					url: finalUrl,
					data: request_packet,
				       	headers: {'Content-Type': 'application/x-www-form-urlencoded'}	
				}).success(function(data){
					deferred.resolve(data);
				}).error(function(){
					deferred.reject("ERROR!");
				});

				_retPromise = deferred.promise.then(function(response){
					
					
					return response; // Do any massaging of response here 	
					
				});

				return _retPromise;


			},



		}
	}




});
