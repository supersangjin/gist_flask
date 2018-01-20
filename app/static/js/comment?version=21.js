var CommentBox = React.createClass({
        loadCommentsFromServer: function() {
            $.ajax({
                url: this.props.url,
                dataType: 'json',
                cache: false,
                success: function(data) {
                    this.setState({data: data});
                }.bind(this),
                error: function(xhr, status, err) {
                    console.error(this.props.url, status, err.toString());
                }.bind(this)
            });
        },
        handleCommentSubmit: function(comment) {
            $.ajax({
                url: this.props.url,
                dataType: 'json',
                type: 'POST',
                data: comment,
                success: function(data) {
                    this.setState({data: data});
                }.bind(this)
            });
        },
        getInitialState: function() {
            return {data: []};
        },
        componentDidMount: function() {
            this.loadCommentsFromServer();
            setInterval(this.loadCommentsFromServer, this.props.pollInterval);
        },
        render: function() {
            if (this.props.auth == "False") {
                return (
                    <div className="commentBox">
                        <CommentList data={this.state.data}/>
                    </div>
                );
            } else {
                return (
                    <div className="commentBox">
                        <CommentForm onCommentSubmit={this.handleCommentSubmit} />
                        <CommentList data={this.state.data}/>
                    </div>
                );
            }
        }
    });

var CommentList = React.createClass({
    render: function() {
        var commentNodes = this.props.data.map(function(comment) {
            return (
                <Comment author={comment.author} key={comment.id} thumbnail={comment.author_thumbnail}>
                    {comment.comment_context}
                </Comment>
            );
        });
        return (
            <div className="commentList">
                {commentNodes}
            </div>
        );
    }
});

var CommentForm = React.createClass({
    getInitialState: function() {
        return {comment_context: ''};
    },
    handleTextChange: function(e) {
        this.setState({comment_context: e.target.value});
    },
    handleSubmit: function(e) {
        e.preventDefault();
        var text = this.state.comment_context.trim();
        if (!text) {
            return;
        }
        this.props.onCommentSubmit({comment_context: text});
        this.setState({comment_context: ''});
    },
    render: function() {
        return (
            <div className="commentForm">
                <form onSubmit={this.handleSubmit}>
                    <textarea className="markdown-body border"
                        type="text"
                        placeholder="Say something..."
                        value={this.state.comment_context}
                        onChange={this.handleTextChange}>
                    </textarea>
                    <button type="submit" value="Post" className="btn btn-success green">Submit</button>
                </form>
            </div>
        );
    }
});

var Comment = React.createClass({
    rawMarkup: function() {
        var md = new Remarkable();
        var rawMarkup = md.render(this.props.children.toString());
        var cleanRawMarkup = DOMPurify.sanitize(rawMarkup);
        return { __html: cleanRawMarkup };
    },

    render: function() {
        var md = new Remarkable();
        return (
                <div className="comment markdown-body border">
                    <div className="post-author">
                        <img className="post-author-thumbnail" src={this.props.thumbnail}/>
                        <div>
                            <a className="post-author-name" href="https://www.google.com" >{this.props.author}</a>
                            <br/>
                            <div className="post-date"> 14 December 2017 </div>
                        </div>
                    </div>
                    <br/>
                    <div>
                        <span dangerouslySetInnerHTML={this.rawMarkup()} />
                    </div>
                </div>
        );
    }
});


var url = document.getElementById('url').value;
var auth = document.getElementById('auth').value;

ReactDOM.render(
    <CommentBox url={url} auth={auth} pollInterval={10000} />,
    document.getElementById('content')
);