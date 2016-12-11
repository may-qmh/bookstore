/**
* AdminController
* @namespace thinkster.layout.controllers
*/
(function () {
  'use strict';

  angular
    .module('thinkster.layout.controllers')
    .controller('AdminController', AdminController);

  AdminController.$inject = ['$scope', '$cookies'];

  /**
  * @namespace NavbarController
  */
  function AdminController($scope, $cookies) {
    
    $scope.tabbed = tabbed;


    var active_tab = $cookies["active_tab"];
    if(active_tab !== undefined){
      switch(active_tab){
        case '1': $scope.tab1 = true; $scope.tab2 = false; $scope.tab3 = false; break;
        case '2': $scope.tab1 = false; $scope.tab2 = true; $scope.tab3 = false; break;
        case '3': $scope.tab1 = false; $scope.tab2 = false; $scope.tab3 = true; break;
        default: $scope.tab1 = true; $scope.tab2 = false; $scope.tab3 = false;
      }
      
    }
    else{
      $scope.tab1 = true; $scope.tab2 = false; $scope.tab3 = false;
    }
    setTimeout(function(){$scope.$apply();},10);
    
    console.log($scope.tab1);
    console.log($scope.tab2);
    console.log($scope.tab3);

    function tabbed(index){
      switch (index){
        case 1: active_tab = 1; break;
        case 2: active_tab = 2; break;
        case 3: active_tab = 3; break;
        default: active_tab = 1;
      }
      $cookies["active_tab"]=index;

    }

  }
})();