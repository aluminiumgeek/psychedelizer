app.controller('HomeCtrl', function($rootScope, $scope, $http, $upload, $location) {
    function get_latest(sort_by) {
        $http({
            url: '/api/get_latest',
            method: 'get'
        }).success(function(data) {
            var images = []
            
            if (!sort_by || (sort_by && sort_by == data.sort_by)) {
                if ($rootScope.latest_images) {
                    $rootScope.latest_images.map(function(item) {
                        images.push(item.src);
                    });
                }
                else {
                    $rootScope.latest_images = [];
                }
            
                var new_items = [];

                data.images.map(function(item) {
                    if (images.indexOf(item.src) == -1) {
                        if (images.length) {
                            $scope.insert_image(item);
                        }
                        else {
                            $rootScope.latest_images.push(item);
                        }
                    }
                });
            }
            else {
                $rootScope.latest_images = data.images;
            }
            
            if (data.client_ip != $scope.client_ip) {
                $scope.client_ip = data.client_ip;
            }
            
            if (data.sort_criterias != $scope.sort_criterias) {
                $scope.sort_criterias = data.sort_criterias;
            }
        })
    }
    
    function get_filters() {
        $http({
            url: '/api/get_filters',
            method: 'get'
        }).success(function(data) {
            $scope.image_filters = data.filters;
        })
    }
    
    function init_websocket() {
        var ws_addr = 'ws://'+location.hostname+':'+location.port+'/updates';
        $scope.ws = new WebSocket(ws_addr);
        
        $scope.ws.onmessage = function (evt) {
            var data = angular.fromJson(evt.data);
            
            if (data.new_image) {
                $scope.insert_image(data.new_image);
            }
        };
    }
    
    $scope.init_ajaxupdater = function() {
        $scope.get_latest_descriptor = setInterval(get_latest, 1500);
    }
    
    $scope.sort_by = 'new';
    
    get_latest();
    get_filters();
    //init_websocket();
    //$scope.init_ajaxupdater();
    
    $scope.clean = function() {
        $scope.original = false;
        $scope.preview = false;
        $scope.selected = [];
    }
    
    $scope.file_selected = function($files) {
        var file = $files[0];
        
        $scope.loading_image = true;
        
        $scope.upload = $upload.upload({
            url: '/api/upload',
            method: 'post',
            file: file
          
        }).success(function(data) {
            $scope.original = data.original;
            $scope.preview = data.preview;
            
            $scope.internet_input = false;
            $scope.url = '';
            
            $scope.loading_image = false;
        });
      
    }

    $scope.loading_image = false;
    $scope.$watch('url', function() {
        $scope.enable_upload_button = $scope.url && $scope.url.match(/^http(.*)\.(jpg|jpeg|png)$/i);
    });
    
    $scope.internet_upload = function() {
        if ($scope.enable_upload_button && !$scope.loading_image) {
            $scope.loading_image = true;
            
            $http({
                url: '/api/upload',
                method: 'post',
                data: {url: $scope.url}
            }).success(function(data) {
                $scope.original = data.original;
                $scope.preview = data.preview;
                
                $scope.internet_input = false;
                $scope.url = '';
                
                $scope.loading_image = false;
            })
        }
        else {
            // show some message
        }
    }
    
    $scope.internet_input_toggle = function() {
        if ($scope.internet_input) {
            $scope.internet_input = false;
        }
        else {
            $scope.internet_input = true;
        }
    }
    
    $scope.selected = [];
    
    $scope.select_filter = function(filter) {
        $scope.loading = true;
      
        if (!$scope.filter_in_selected(filter)) {
            $scope.selected.push(filter);
        }
        else {
            $scope.selected.splice($scope.selected.indexOf(filter), 1);
        }
        
        $http({
            url: '/api/preview',
            method: 'post',
            data: {
                preview: $scope.preview, 
                original: $scope.original,
                filters: $scope.selected,
                combine: $scope.use_pattern,
            }
        }).success(function(data) {
            $scope.preview = data.preview;
            $scope.loading = false;
        })
    }
    
    $scope.filter_in_selected = function(filter) {
        if ($scope.selected.indexOf(filter) == -1) {
            return false;
        }
        else {
            return true;
        }
    }
    
    $scope.save = function() {
        if ($scope.selected.length) {
            $http({
                url: '/api/save',
                method: 'post',
                data: {image: $scope.preview}
            }).success(function(data) {
                clearInterval($scope.get_latest_descriptor);
                
                $scope.saved_image = data.new_image;
                $scope.clean();
                
                //$scope.$apply(function() {
                    var src = $scope.saved_image.src;
                    var image_link = src.substr(0, src.lastIndexOf('.'));
                    
                    $location.path('/image/' + image_link);
                //});
            })
        }
    }
    
    $scope.insert_image = function(image) {
        image.created = true;
        
        $rootScope.latest_images.unshift(image);
        
        setTimeout(
            function() {
                var index = $rootScope.latest_images.indexOf(image);
                $scope.latest_images[index].created = false;
                $scope.$apply();
            },
            400
        );
    }
    
    $scope.use_pattern = false;
    
    $scope.like = function(image) {
        $http({
            url: '/api/like',
            method: 'post',
            data: {image: image}
        }).success(function(data) {
            var index = $rootScope.latest_images.indexOf(image);
            $rootScope.latest_images[index].likes = data.likes;
        })
    }
    
    $scope.show_likes = false;
    
    $scope.set_sort_by = function(criteria) {
        switch (criteria) {
            case 'new':
                if ($scope.sort_by != criteria) {
                    $scope.show_likes = false;
                  
                    get_latest($scope.sort_by);
                    $scope.sort_by = criteria;
                    $scope.init_ajaxupdater();
                }
                break;
            case 'best':
            default:
                if ($scope.sort_by != criteria) {
                    $scope.sort_by = criteria;
                    clearInterval($scope.get_latest_descriptor);
                    
                    $http({
                        url: '/api/get_latest',
                        method: 'post',
                        data: {sort_by: criteria}
                    }).success(function(data) {
                        $rootScope.latest_images = data.images;
                        $scope.show_likes = true;
                    })
                }
        }
    }
    
});

app.controller('ImageCtrl', function($rootScope, $scope, $http, $routeParams) {
    $scope.unixtime = $routeParams.unixtime;
    
    $http({
            url: '/api/get_latest',
            method: 'get'
    }).success(function(data) {
        $scope.client_ip = data.client_ip;
    });
    
    $http({
        url: '/api/image/'+$scope.unixtime,
        method: 'get',
    }).success(function(data) {
        $scope.image = data;
    });

    $scope.like = function(image) {
        $http({
            url: '/api/like',
            method: 'post',
            data: {image: image}
        }).success(function(data) {
            $scope.image.likes = data.likes;
            
            $rootScope.latest_images.map(function(item) {
                if (item.unixtime == image.unixtime) {
                    item.likes = data.likes;
                }
            });
        })
    }
    
});
