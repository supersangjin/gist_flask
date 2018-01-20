var FilteredList = React.createClass({
    filterList: function(event){
        if (event.target.value){
            // TODO get book list
            let updatedList = [];
            let self = this;
            $.ajax({
                url: 'https://www.googleapis.com/books/v1/volumes?key=AIzaSyCZDeUzMo21vkKpPQBAFwSdle6RkkACWKA&fields=items&q=+intitle:' + event.target.value + '&orderBy=relevance',
                dataType: 'json',
                success: function(data) {
                    for (let i = 0; i < data.items.length; i++){
                        let item = data.items[i];
                        let book = {
                            id : item.id,
                            title : item.volumeInfo.title,
                            authors : item.volumeInfo.authors,
                            publisher : item.volumeInfo.publisher,
                            categories : item.volumeInfo.categories,
                            thumbnail : item.volumeInfo.imageLinks.thumbnail
                        };
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
    selectBook: function() {
        this.setState({items: []});

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
                <List items={this.state.items} selectBook={this.selectBook} />
            </div>
        );
    }
});

var List = React.createClass({
    render: function(){
        let self = this;
        return (
            <ul className="list-group search-list">
            {
                this.props.items.map(function(item) {
                    return <li className="list-group-item" key={item.id} onClick={self.props.selectBook}>
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
