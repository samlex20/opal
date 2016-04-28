angular.module('opal.services')
    .factory('patientLoader', function($q, $window, $http, $route, Episode, recordLoader, FieldTranslater) {
        return function() {
          "use strict";
	        var deferred = $q.defer();
            var patient_id = $route.current.params.patient_id;
            if(!patient_id){
                deferred.resolve([]);
            }
            var target = "/api/v0.1/patient/" + patient_id + '/';
            var getEpisodePromise = $http.get(target);


            $q.all([recordLoader, getEpisodePromise]).then(
                    function(results)   {
                        var patient = results[1].data;
                        patient = FieldTranslater.patientToJs(patient);
                        patient.episodes = _.map(patient.episodes, function(resource) {
                            return new Episode(resource);
                        });

                        var episodeValues = _.values(patient.episodes);
                        if(episodeValues.length){
                          _.each(patient, function(v, k){
                              if(k in episodeValues[0]){
                                  patient[k] = episodeValues[0][k];
                              }
                          });
                          patient.recordEditor = episodeValues[0].recordEditor;
                        }

                        deferred.resolve(patient);
                    }, function() {
                        // handle error better
                        $window.alert('Episodes could not be loaded');
              });
	        return deferred.promise;
        };
    });
