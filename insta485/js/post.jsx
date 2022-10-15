import React from "react";
import PropTypes from "prop-types";

class Post extends React.Component {
  /* Display image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { imgUrl: "", owner: "" };
  }

  /* 
  {
  "comments": [
    {
      "commentid": 1, 
      "lognameOwnsThis": true, 
      "owner": "awdeorio", 
      "ownerShowUrl": "/users/awdeorio/", 
      "text": "#chickensofinstagram", 
      "url": "/api/v1/comments/1/"
    }, 
    {
      "commentid": 2, 
      "lognameOwnsThis": false, 
      "owner": "jflinn", 
      "ownerShowUrl": "/users/jflinn/", 
      "text": "I <3 chickens", 
      "url": "/api/v1/comments/2/"
    }, 
    {
      "commentid": 3, 
      "lognameOwnsThis": false, 
      "owner": "michjc", 
      "ownerShowUrl": "/users/michjc/", 
      "text": "Cute overload!", 
      "url": "/api/v1/comments/3/"
    }
  ], 
  "comments_url": "/api/v1/comments/?postid=3", 
  "created": "2022-10-15 04:30:36", 
  "imgUrl": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg", 
  "likes": {
    "lognameLikesThis": true, 
    "numLikes": 1, 
    "url": "/api/v1/likes/6/"
  }, 
  "owner": "awdeorio", 
  "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg", 
  "ownerShowUrl": "/users/awdeorio/", 
  "postShowUrl": "/posts/3/", 
  "postid": 3, 
  "url": "/api/v1/posts/3/"
}
  */

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          ownerImgUrl: data.ownerImgUrl,
          owner: data.owner,
          created: data.created,
          imgUrl: data.imgUrl,
          // numLikes = data.likes['numLikes'],

          

          
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { imgUrl, owner } = this.state;
    // Render post image and post owner
    // return (
      /* <div className="post">
        <p>{owner}</p>
        <p>{ownerImgUrl}</p>
        <img src={imgUrl} alt="post_image" />
        
      </div> */
    const myElement = (
      <div>
        <div class="card border-dark mb-3 mx-auto" style="max-width: 40rem;"></div>
        <div class="card-header bg-transparent border-dark"> <a href="/users/{owner}/"><img
                    src={ownerImgUrl} alt="{post.owner} profile pic" class="rounded-circle"
                    style="width:5%;"></a> <a href="/users/{{ post.owner }}/"><b>{{ post.owner }}</b></a> <small
                class="text-muted"><a href="/posts/{{ post.postid }}/" style="all:unset;"> {{ post.timestamp }} </a>
            </small></div>
        <div class="card-body text-dark">
            <a href="/posts/{{ post.postid }}/"><img src="{{ post.img_url }}" class="card-img-bottom"
                    alt="{{ post.owner }} picture"></a>
        </div>
        <div class="card-footer bg-transparent border-dark">
            <p>{{ post.likes }} {% if post.likes == 1 -%} like {%- else -%} likes {%- endif %} </p>
            {% for comment in post.comments %}
            <p> <a href="/users/{{ comment.owner }}/"> <b>{{ comment.owner }}</b></a> {{ comment.text }}</p>
            {% endfor %}
        </div>
        <hr>
        <div class="like-comment">
            {% if post.is_liked %}
            <form action="{{url_for('update_like', target='/')}}" method="post" enctype="multipart/form-data" className="like-unlike-button">
                <input type="hidden" name="operation" value="unlike" />
                <input type="hidden" name="postid" value="{{ post.postid }}" />
                <input type="submit" name="unlike" value="unlike" />
            </form>
            {% else %}
            <!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') --
            <form action="{{url_for('update_like', target='/')}}" method="post" enctype="multipart/form-data" className="like-unlike-button">
                <input type="hidden" name="operation" value="like" />
                <input type="hidden" name="postid" value="{{ post.postid }}" />
                <input type="submit" name="like" value="like" />
            </form>
            {% endif %}
            <br>
            <!-- DO NOT CHANGE THIS (aside from where we say 'FIXME') --
            <form action="{{url_for('update_comment', target='/')}}" method="post" enctype="multipart/form-data" className="comment-form">
                <input type="hidden" name="operation" value="create" />
                <input type="hidden" name="postid" value="{{ post.postid }}" />
                <input type="text" name="text" required />
                <input type="submit" name="comment" value="comment" />
            </form>
        </div>
        
      </div>
      
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;


{/* owner img
owner link
timestamp
post img
likes
  comment owner url
  comment
unlike post
delete comment  */}

