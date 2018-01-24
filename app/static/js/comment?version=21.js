var CommentBox = React.createClass({
        loadCommentsFromServer: function() {
            $.ajax({
                url: this.props.addUrl,
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
                url: this.props.addUrl,
                dataType: 'json',
                type: 'POST',
                data: comment,
                success: function(data) {
                    this.setState({data: data});
                    this.loadCommentsFromServer();
                }.bind(this)
            });
        },
        handleCommentDelete: function(comment) {
            $.ajax({
                url: this.props.deleteUrl,
                dataType: 'json',
                type: 'POST',
                data: comment,
                success: function(data) {
                    this.setState({data: data});
                }.bind(this)
            })
        },
        getInitialState: function() {
            return {data: [], offset: 5};
        },
        componentDidMount: function() {
            this.loadCommentsFromServer();
        },
        onClickButton: function() {
            var COMMENT_VIEW_LENGTH = 5;
            this.setState({offset: this.state.offset + COMMENT_VIEW_LENGTH});
            if (this.state.offset >= this.state.data.length) {
                document.getElementById("button-id").style.display = "none";
            }
        },
        render: function() {
            if (this.props.auth == "False") {
                return (
                    <div className="commentBox">
                        <CommentList data={this.state.data.slice(0, this.state.offset)} />
                        <button id="button-id" className="btn btn-sm btn-secondary" onClick={this.onClickButton}>More comment</button>
                    </div>
                );
            } else {
                return (
                    <div className="commentBox">
                        <CommentForm onCommentSubmit={this.handleCommentSubmit} />
                        <CommentList data={this.state.data.slice(0, this.state.offset)} onCommentDelete={this.handleCommentDelete} currentUserId={this.props.currentUserId}/>
                        <button id="button-id" className="btn btn-sm btn-secondary" onClick={this.onClickButton}>More comment</button>
                    </div>
                );
            }
        }
    });

var CommentList = React.createClass({
    render: function() {
        self = this
        var commentNodes = this.props.data.map(function(comment) {
            return (
                <Comment key={comment.id} comment={comment} _delete={self.props.onCommentDelete} currentUserId={self.props.currentUserId}>
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
                        placeholder="What do you think about this?"
                        value={this.state.comment_context}
                        onChange={this.handleTextChange}>
                    </textarea>
                    <button type="submit" value="Post" className="btn btn-sm btn-secondary">Post comment</button>
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
    deleteComment: function() {
        this.props._delete({
            id: this.props.comment.id
        })
    },
    render: function() {
        var md = new Remarkable();
        if (this.props.currentUserId == this.props.comment.author_id){
            return (
                    <div className="comment markdown-body border">
                        <div className="post-author">
                            <img className="post-author-thumbnail" src={this.props.comment.author_thumbnail}/>
                            <div>
                                <a className="post-author-name" href={'/user_profile/' + this.props.comment.author_id}>{this.props.comment.author}</a>
                                <br/>
                                <div className="post-date"> {this.props.comment.comment_creDate} </div>
                            </div>
                        </div>
                        <div>
                            <span dangerouslySetInnerHTML={this.rawMarkup()} />
                        </div>
                        <a onClick={this.deleteComment}>delete</a>
                    </div>

            );
        } else {
            return (
                    <div className="comment markdown-body border">
                        <div className="post-author">
                            <img className="post-author-thumbnail" src={this.props.comment.author_thumbnail}/>
                            <div>
                                <a className="post-author-name" href={'/user_profile/' + this.props.comment.author_id}>{this.props.comment.author}</a>
                                <br/>
                                <div className="post-date"> {this.props.comment.comment_creDate} </div>
                            </div>
                        </div>
                        <div>
                            <span dangerouslySetInnerHTML={this.rawMarkup()} />
                        </div>
                    </div>
            );
        }
    }
});

var addUrl = document.getElementById('addUrl').value;
var deleteUrl = document.getElementById('deleteUrl').value;
var auth = document.getElementById('auth').value;
var currentUserId = document.getElementById('currentUserId').value;

ReactDOM.render(
    <CommentBox addUrl={addUrl} deleteUrl={deleteUrl} auth={auth} currentUserId={currentUserId} />,
    document.getElementById('content')
);