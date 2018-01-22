var FilteredList = React.createClass({
    filterList: function(event){
        if (event.target.value){
            $.ajax({
                url: this.props.searchUrl,
                type: 'POST',
                dataType: 'json',
                data: {"term": event.target.value},
                cache: false,
                success: function(data) {
                    this.setState({items: data});
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this)
            });
        } else {
            this.setState({items: []});
        }
    },
    selectBook: function(query) {
        console.log(query)
        document.getElementById("searchFilterForm").query.value = query;
        document.getElementById("searchFilterForm").submit();
    },
    getInitialState: function(){
        return {
            items: []
        };
    },
    componentWillMount: function(){
        this.setState({items: []});
    },
    render: function(){
        return (
            <div className="filter-list">
                <form id="searchFilterForm" action={this.props.submitUrl} autoComplete="off" >
                    <fieldset className="form-group">
                        <input type="text" name="query" className="form-control form-control-lg" placeholder="Search Book" onChange={this.filterList}/>
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
                    return <li className="list-group-item" key={item.id} onClick={() => self.props.selectBook(item.title)}>
                                <img src={item.thumbnail} style={{ width: 'auto', height: '50px' }}/>
                                {item.title} &nbsp; {item.authors}
                            </li>
                })
            }
            </ul>
        )
    }
});

var submitUrl = document.getElementById('submitUrl').value;
var searchUrl = document.getElementById('searchUrl').value;

ReactDOM.render(
    <FilteredList searchUrl={searchUrl} submitUrl={submitUrl}/>,
    document.getElementById('search')
);
