/* eslint-disable react/prop-types */
/* eslint-disable react/prefer-stateless-function */
/* eslint-disable max-classes-per-file */
import React from "react";
import { createRoot } from "react-dom/client";
import moment from "moment";
// import PropTypes from "prop-types";

// import Post from "./post";
//

function Likes(props) {
  const { numLikes, lognameLikesThis } = this.props;
  let likeButton;
  if (lognameLikesThis) {
    likeButton = (
      <button
        type="button"
        className="like-unlike-button"
        onClick={this.handleClick}
      >
        Unlike
      </button>
    );
  } else {
    likeButton = (
      <button
        type="button"
        className="like-unlike-button"
        onClick={this.handleClick}
      >
        Like
      </button>
    );
  }
  console.log("number likes: ", numLikes);
  console.log("logname likes: ", lognameLikesThis);
  let likeText;
  if (numLikes === 0 || numLikes > 1) {
    likeText = <p> {numLikes} likes</p>;
  } else {
    likeText = <p> {numLikes} like </p>;
  }
  return (
    <div>
      {likeText}
      {likeButton}
    </div>
  );
}

// Likes.propTypes = {
//   numLikes: PropTypes.number,
//   lognameLikesThis: PropTypes.bool,
// };

function Comment(props) {
  const { owner, text } = this.props;
  return (
    <>
      <p>
        <b>{owner}</b>
      </p>{" "}
      <p>{text}</p>
    </>
  );
}

// Comment.propTypes = {
//   owner: PropTypes.string,
//   text: PropTypes.string,
// };

class CommentSection extends React.Component {
  render() {
    const { comments } = this.props;
    return (
      <div>
        {comments.map((comment) => (
          <Comment owner={comment.owner} text={comment.text} />
        ))}
        <form className="comment-form">
          <input type="text" name="text" required />
          <input type="submit" name="comment" value="comment" />
        </form>
      </div>
    );
  }
}

// CommentSection.propTypes = {
//   comments: PropTypes.arrayOf,
// };

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.state = {
      isLiked: this.lognameLikesThis,
      numLikes: this.numLikes,
    };
  }

  handleClick() {
    this.setState((prevState) => ({
      numLikes: isLiked ? numLikes - 1 : numLikes + 1,
      isLiked: !prevState.isLiked,
    }));
  }

  render() {
    const { api } = this.props;
    const dateToFormat = api.created;
    // const moment = require("moment");
    let timestamp = moment.utc(dateToFormat);
    timestamp = moment().fromNow(timestamp);

    return (
      <div>
        <a href={api.ownerShowUrl}>
          {" "}
          <img src={api.ownerImgUrl} alt="post-pic" />{" "}
        </a>
        <a href={api.ownerShowUrl}> {api.owner} </a>
        <a href={api.postShowUrl}>
          <p> {timestamp} </p>
        </a>
        <img src={api.imgUrl} alt="post-pic" />
        <Likes
          numLikes={api.likes.numLikes}
          lognameLikesThis={api.likes.lognameLikesThis}
        />
        <CommentSection comments={api.comments} />
      </div>
    );
  }
}

class Feed extends React.Component {
  constructor(props) {
    super(props);
    this.state = { posts: [] };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    const entry = document.getElementById("reactEntry");
    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log("data results: ", data.results);
        const div = document.createElement("div");
        entry.appendChild(div);
        data.results.map((post) =>
          fetch(post.url, { credentials: "same-origin" })
            .then((response2) => {
              if (!response2.ok) throw Error(response2.statusText);
              return response2.json();
            })
            .then((data2) => {
              console.log(data2);
              this.setState({ posts: this.state.posts.concat(data2) });
            })
            .catch((error) => console.log(error))
        );
      });
  }

  render() {
    const { posts } = this.state;
    console.log("post results: ", posts);
    return (
      <div>
        {posts.map((post) => (
          <div>
            <Post api={post} />
          </div>
        ))}
      </div>
    );
  }
}

// Create a root
const root = createRoot(document.getElementById("reactEntry"));
// This method is only called once
// Insert the post component into the DOM

root.render(<Feed url="/api/v1/posts/" />);

// .map((post) =>
//             fetch(post.url, { credentials: "same-origin" })
//               .then((response2) => {
//                 if (!response2.ok) throw Error(response2.statusText);
//                 return response2.json();
//               })
//               .then((data2) => {
//                 console.log(data2);
//                 this.setState({ posts: this.state.posts.concat(data2) });
//               })
//           )
