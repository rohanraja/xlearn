'use strict';

angular.module('sbAdminApp')
  .service('listservice', function(serverComm) {


    this.loadDatasets = function(){

      var out = [
         {
            name : 'Nepal Data English',
            models : [
              {
                id : '0',
                name : 'RNN 2 layer',
                params : [0,1,2],
    
              },
              {
                id : '1',
                name : 'SVM radial',
                params : [0,1,2],
              }
            ]
          },

          {
            name : 'Nepal Data Hindi',
            models : [
              {
                id : '0',
                name : 'RNN 3 layer'
              },
              {
                id : '1',
                name : 'SVM linear'
              }
           ]
          }

         ];

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
                id: 2,
                name: "LSTM"
              }
              
            ]
      return out

    };
  });
