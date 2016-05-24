(function() {
    (function($) {
        return $.widget('IKS.blockquotebutton', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;
 
                widget = this;
 
                button = $('<span></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Block Quote / Tabbed Text',
                    icon: 'fa fa-indent',
                    command: null
                });
 
                toolbar.append(button);
 
                button.on('click', function(event) {
                    return widget.options.editable.execute('formatBlock',
                                                           'blockquote');
                });
            }
        });
    })(jQuery);
}).call(this);
 
(function() {
  (function($) {
    return $.widget("IKS.blockquotebuttonwithclass", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;
 
        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Pull Quote',
          icon: 'fa fa-quote-left',
          command: null
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var insertionPoint, lastSelection;
 
          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var elem;
                    elem = "<blockquote class='pullquote'>" + lastSelection + "</blockquote>";
 
                    var node = lastSelection.createContextualFragment(elem);
 
                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);
 
                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);
 
}).call(this);