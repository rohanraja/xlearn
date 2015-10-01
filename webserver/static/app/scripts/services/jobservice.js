'use strict';

angular.module('sbAdminApp')
  .service('jobservice', function(serverComm) {

    this.getModelInfo = function(modelId) {

      var query = {
        'type': 'getModelInfo',
        'params': {
          'modelId': modelId
        }
      };

      var defer = serverComm.getData(query);
      return defer;

    };

    this.getParamsInfo = function(modelId, paramsId) {

      var out = {
      
      modelid: 1,
      paramid: 1,
      learn_embedding: 1,
      
      model: {
        input: "100",
        L1_output: "200",
        output:"100"
      },

      optimizer: {
        name: 'sgd',
        alpha: 0.1,
        decay: 0.001,
        batch_size: 10,
      }
    };
      var query = {
        'type': 'getParamsInfo',
        'params': {
          'modelId': modelId,
          'paramsId': paramsId,
        }
      };

      var defer = serverComm.getData(query);
      return defer;
    };



    this.createParams = function(modelId, paramsInfo){

      var query = {
        'type': 'createParamsInfo',
        'params': {
          'modelId': modelId,
          'pInfo': paramsInfo,
        }
      };

      var defer = serverComm.getData(query);

      return defer ;

    };

    this.createModel = function(jobInfo, paramsInfo){

      return [newmodelId, newparamsId];
    };


});
