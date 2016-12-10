/**
* Authentication
* @namespace thinkster.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('thinkster.authentication.services')
    .factory('ShareVar',ShareVar);

  ShareVar.$inject = ['$http'];

  function ShareVar($http){

  	var ShareVar = {
      search_books:search_books,
      get_book_info:get_book_info,
      order_book: order_book
  	};
  	
  	return ShareVar;

    function search_books(author,publisher,bk_title,subject) {
      return $http.post('/search/',{
        author: author,
        publisher: publisher,
        bk_title: bk_title,
        subject: subject
      }).then(searchSuccessFn, searchErrorFn);

      function searchSuccessFn(data, status, headers, config) {
        console.log("success")

        window.location = '/search';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function searchErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
    */
    function get_book_info(isbn10) {
      return $http.post('/book/'+isbn10,{
        isbn10: isbn10
      }).then(bookSuccessFn, bookErrorFn);

      function bookSuccessFn(data, status, headers, config) {
        console.log("success")

        window.location = '/book/'+isbn10;
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function bookErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    /**
      * @name logoutErrorFn
      * @desc Log "Epic failure!" to the console
    */
    function order_book(isbn10,n) {
      return $http.post('/confirmation/'+isbn10,{
        isbn10: isbn10,
        n: n
      }).then(bookSuccessFn, bookErrorFn);

      function bookSuccessFn(data, status, headers, config) {
        console.log("success")

        window.location = '/confirmation/'+isbn10;
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function bookErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
        window.alert('Please log in/ register before ordering any books!')
        //window.location = '/book/'+isbn10
      }
    }
  };
})()