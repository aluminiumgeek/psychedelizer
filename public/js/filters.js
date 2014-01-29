
app.filter('remove_ext', function() {
    return function(text) {
        if (text !== undefined) {
            return text.substr(0, text.lastIndexOf('.'));
        }
    };
});

app.filter('extract', function() {
    return function(date, type) {
        if (date !== undefined) {
            switch (type) {
                case 'time':
                    return date.split(' ')[1];
                case 'date':
                    return date.split(' ')[0];
            }
        }
    }
});
