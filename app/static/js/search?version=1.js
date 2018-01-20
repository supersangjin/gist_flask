var FilteredList = React.createClass({
    filterList: function(event){
        if (event.target.value){
            // TODO get book list
            var updatedList = [];
            var self = this;
            $.ajax({
                url: 'https://www.googleapis.com/books/v1/volumes?key=AIzaSyCZDeUzMo21vkKpPQBAFwSdle6RkkACWKA&fields=items&q=+intitle:' + event.target.value + '&orderBy=relevance',
                dataType: 'json',
                success: function(data) {
                    for (let i = 0; i < data.items.length; i++){
                        let item = data.items[i].volumeInfo;
                        let book = {
                            id : item.id,
                            title : item.title,
                            authors : item.authors,
                            publisher : item.publisher,
                            publishedDate : item.publishedDate,
                            description : item.description,
                            categories : item.categories,
                            thumbnail : item.imageLinks.thumbnail
                        }
                        updatedList.push(book);
                    }
                    self.setState({items: updatedList});
                },
                type: 'GET'
            });
        } else {
            this.setState({items: []});
        }
    },
    getInitialState: function(){
        return {
            items: []
        }
    },
    componentWillMount: function(){
        this.setState({items: []})
    },
    render: function(){
        return (
            <div className="filter-list">
                <form>
                    <fieldset className="form-group">
                        <input type="text" className="form-control form-control-lg" placeholder="Search Book" onChange={this.filterList}/>
                    </fieldset>
                </form>
                <List items={this.state.items}/>
            </div>
        );
    }
});

var List = React.createClass({
    render: function(){
        return (
            <ul className="list-group search-list">
            {
                this.props.items.map(function(item) {
                    return <li className="list-group-item" key={item.id}>
                                <img src={item.thumbnail} style={{ width: 'auto', height: '50px' }}/>
                                {item.title} &nbsp; {item.authors}
                            </li>
                })
            }
            </ul>
        )
    }
});


ReactDOM.render(
    <FilteredList />,
    document.getElementById('search')
);
