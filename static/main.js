Ext.BLANK_IMAGE_URL = '/static/extjs/resources/images/default/s.gif';
Ext.ns('ExtNS');

// main object for all application related storagies etc
App = {};

// application main entry point
Ext.onReady(function() {
    Ext.QuickTips.init();

    //==========================
    if (document.getElementById('notes-list__controls')) {
        NotesListControls.init();
    }

}); // eo function onReady

var NotesListControls = {
    currentPage: 1,
    tagIds: {
        controlsContainer: 'notes-list__controls',
        listContainer: 'notes-list',
        paginationContainer: 'notes-list__pagination'
    },

    init: function() {
        this.createFiltersAndSorts();
        this.setLoadMoreButtonHandler();
    },

    createFiltersAndSorts : function() {        
        if (typeof(App.noteCategories) === "undefined") {
            App.noteCategories = [['all', 'все']];
        }
        App.filtersForm = new Ext.form.FormPanel({
            //renderTo: this.tagIds.controlsContainer,            
            width: 600,
            frame: true,
            title: 'Фильтры и сортировка',            
            padding: 10,
            labelWidth: 120,
            labelAlign: 'left',
            layout: 'form',
            
            items: [
                {
                    xtype: 'panel',
                    layout: 'column',
                    items: [{
                        layout: 'form',
                        columnWidth: 0.5,
                        items: [{
                            xtype: 'datefield',
                            //~ width: 120,
                            fieldLabel: 'Начало периода',
                            name: 'date_from',
                            format: 'd/m/Y',
                            anchor: '95%'
                        }]
                        
                    }, {
                        layout: 'form',
                        columnWidth: 0.5,
                        items: [{
                            xtype: 'datefield',
                            //~ width: 120,
                            fieldLabel: 'Конец периода',
                            name: 'date_to',
                            format: 'd/m/Y',
                            anchor: '95%'
                        }]
                    }]
                }, {
                    xtype: 'textfield',
                    fieldLabel: 'Заголовок',
                    name: 'title',
                    width: '95%',
                    maxLength: 100
                }, {
                    xtype: 'panel',
                    layout: 'column', 
                    items: [{
                        layout: 'form',
                        columnWidth: 0.5,
                        items: [{                            
                            xtype: 'combo',
                            fieldLabel: 'Категория',
                            name: 'x_category',
                            hiddenName: 'category',
                            store: App.noteCategories,                                                            
                            triggerAction: 'all',
                            //~ width: 140,
                            anchor: '95%'
                        }, {
                            xtype: 'combo',
                            fieldLabel: 'Сортировка',
                            name: 'x_sort',
                            id: 'x_sort',
                            hiddenName: 'sort',
                            store: new Ext.data.ArrayStore({
                                id: 0,
                                fields: [
                                    'fieldValue',  
                                    'displayText'
                                ],
                                data: [
                                    ['date_desc', 'последние'],
                                    ['date_asc', 'первые'],
                                    ['category', 'по категории'],
                                    ['favorite', 'избранные']
                                ]
                            }),
                            valueField: 'fieldValue',
                            displayField: 'displayText',
                            allowBlank: false,
                            editable: false,
                            typeAhead: false,
                            triggerAction: 'all',
                            mode: 'local',
                            //~ width: 140,
                            anchor: '95%'
                        }]
                    }, {
                        layout: 'form',
                        columnWidth: 0.5,
                        items: [{
                            xtype: 'checkbox',
                            fieldLabel: 'Только избранные',
                            name: 'favorite'
                        }]
                    }]
                }
            ],
            
            buttons: [{
                text: 'Применить',
                name: 'submit',
                formBind: true,
                handler: function(btn, evt){
                    NotesListControls.currentPage = 1;
                    App.filtersForm.getForm().submit({
                        method: 'GET',
                        // nice naming from sencha btw
                        failure: function(form, response) {                            
                            // console.log(response);
                            var html = response.response.responseText;
                            Ext.get('notes-list').update(html);
                            NotesListControls.setLoadMoreButtonVisibility(response);
                        }
                    });
                }
            }]
        });
        
        Ext.getCmp('x_sort').setValue('date_desc');
        App.filtersForm.render(this.tagIds.controlsContainer);
    },
    
    setLoadMoreButtonHandler: function() {
        var loadMoreButtonDom = Ext.DomQuery.select('.notes-list__load-more-button');
        var el = Ext.get(loadMoreButtonDom[0]);
        el.on('click', function(){
            var nextPage = NotesListControls.currentPage + 1;
            //console.log(nextPage);
            App.filtersForm.getForm().submit({                
                method: 'GET',
                params: {
                    page: nextPage
                },
                failure: function(form, response) {                            
                    // console.log(response);
                    var html = response.response.responseText;
                    var list = Ext.get('notes-list');
                    var currentHtml = list.dom.innerHTML;
                    var newHtml = currentHtml + html;
                    list.update(newHtml);
                    NotesListControls.setLoadMoreButtonVisibility(response);
                    NotesListControls.currentPage = nextPage;
                }
            });
            
        });
    },
    
    setLoadMoreButtonVisibility: function(response) {
        var end_of_collection = response.response.getResponseHeader('X-End-Of-Collection');        
        var loadMoreButtonDom = Ext.DomQuery.select('.notes-list__load-more-button');
        var el = Ext.get(loadMoreButtonDom[0]);       
        if (end_of_collection === '1') {
            Ext.fly(el).addClass('none');
        } else {
            Ext.fly(el).removeClass('none');
        }
    } 
}


