 $(function() {
          $('a#test').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/like',
                function(data) {
              //do nothing
            });
            return false;
          });
        });