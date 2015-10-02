'use strict';

angular.module('sbAdminApp')
  .service('listservice', function(serverComm) {


    this.loadDatasets = function(){

      var query = {
        'type': 'loadDatasets',
        'params': {
        }
      };

      var defer = serverComm.getData(query);

      return defer ;
    };

    this.loadMappers = function($modelid){

      var out = [
        {
          id: 1,
          name: "Self Vocab"
        },
        {
          id: 2,
          name: "Cat to Numerical"
        }
        
      ]
      return out

    };


    this.loadEmbeddings = function($modelid){

            var out = [
              {
                id: 0,
                name: "Gaussian"
              },
              {
                id: 2,
                name: "Word2Vec"
              }
              
            ];
      return out

    };

    this.loadModels = function($modelid){

            var out = [
              {
                id: 0,
                name: "RNN"
              },
              {
                id: 3,
                name: "MLP_QUANT"
              }
              
            ]
      return out

    };
  });
