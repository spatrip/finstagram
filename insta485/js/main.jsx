import React from "react";
import { createRoot } from "react-dom/client";
// import Post from "./post";

class Likes extends React.Component {
  render() {
    const numLikes = this.props.numLikes;
    const lognameLikesThis = this.props.lognameLikesThis;
    let likeButton;
    if (lognameLikesThis) {
      likeButton = <button type="button">Unlike</button>;
    } else {
      likeButton = <button type="button">Like</button>;
    }
    let likeText;
    if (numLikes === 0 || numLikes > 1) {
      likeText = <p> {numLikes} likes</p>;
    } else {
      likeText = <p> {numLikes} like </p>;
    }
    return (
      <div>
          {likeText}
          <br>
          {likeButton}
      </div>
    );
  }
}

class Comment extends React.Component {
    render(){
        const owner = this.props.owner;
        const text = this.props.text;
        return (
            <>
            <p><b>{owner}</b></p> <p>{text}</p>
            </>
        );
    }
}

class CommentSection extends React.Component {
    render(){
        const comments = this.props.comments;
        return(
            <div>
                {comments.map((comment, i) => <Comment owner={comment.owner} text={comment.text} key={i}/>)}
                <form enctype="multipart/form-data" className="comment-form">
                    <input type="text" name="text" required />
                    <input type="submit" name="comment" value="comment" />
                </form>
            </div>
        );
    }
}

const API = [
  {
    comments: [
      {
        commentid: 1,
        lognameOwnsThis: true,
        owner: "awdeorio",
        ownerShowUrl: "/users/awdeorio/",
        text: "#chickensofinstagram",
        url: "/api/v1/comments/1/",
      },
      {
        commentid: 2,
        lognameOwnsThis: false,
        owner: "jflinn",
        ownerShowUrl: "/users/jflinn/",
        text: "I <3 chickens",
        url: "/api/v1/comments/2/",
      },
      {
        commentid: 3,
        lognameOwnsThis: false,
        owner: "michjc",
        ownerShowUrl: "/users/michjc/",
        text: "Cute overload!",
        url: "/api/v1/comments/3/",
      },
    ],
    comments_url: "/api/v1/comments/?postid=3",
    created: "2022-10-15 04:30:36",
    imgUrl: "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
    likes: {
      lognameLikesThis: true,
      numLikes: 1,
      url: "/api/v1/likes/6/",
    },
    owner: "awdeorio",
    ownerImgUrl: "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
    ownerShowUrl: "/users/awdeorio/",
    postShowUrl: "/posts/3/",
    postid: 3,
    url: "/api/v1/posts/3/",
  },
];

// Create a root
const root = createRoot(document.getElementById("reactEntry"));
// This method is only called once
// Insert the post component into the DOM

root.render(<Post url="/api/v1/posts/3/" />);
