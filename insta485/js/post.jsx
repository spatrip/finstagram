import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Likes from "./likes";
// import CommentSection from "./comment-section";
import CommentForm from "./comment-section";

class Post extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      ownerImgUrl: "",
      owner: "",
      ownerShowUrl: "",
      postShowUrl: "",
      created: "",
      imgUrl: "",
      comments: [{ owner: "", text: "" }],
      likes: { lognameLikesThis: null, numLikes: null, url: "" },
      value: "",
    };
    this.handleLike = this.handleLike.bind(this); //
    this.handleUnlike = this.handleUnlike.bind(this); //
    this.handleSub = this.handleSub.bind(this); //
    this.handleCha = this.handleCha.bind(this); //
    this.handlePostLike = this.handlePostLike.bind(this); //
  }

  componentDidMount() {
    console.log("component did mount ran");
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log("data: ", data);
        this.setState({
          ownerImgUrl: data.ownerImgUrl,
          owner: data.owner,
          imgUrl: data.imgUrl,
          created: data.created,
          likes: data.likes,
          comments: data.comments,
          postShowUrl: data.postShowUrl,
          ownerShowUrl: data.ownerShowUrl,
          postid: data.postid,
        });
      })
      .catch((error) => console.log(error));
    let postImg = document.getElementById("postimg");
    postImg.addEventListener("dblclick", this.handleLike);
  }

  handleLike(e) {
    e.preventDefault();
    if (this.state.likes.lognameLikesThis) {
      console.log("already liked");
    } else {
      fetch(`/api/v1/likes/?postid=${this.state.postid}`, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState((prevState) => ({
            likes: {
              numLikes: prevState.likes.numLikes + 1,
              lognameLikesThis: !prevState.likes.lognameLikesThis,
              url: data.url,
            },
          }));
        })
        .catch((error) => console.log(error));
    }
  }

  handleUnlike(e) {
    e.preventDefault();

    fetch(this.state.likes.url, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        // return response.json();
      })
      .then((data) => {
        console.log("unlike data: ", data);
        this.setState((prevState) => ({
          likes: {
            numLikes: prevState.likes.numLikes - 1,
            lognameLikesThis: !prevState.likes.lognameLikesThis,
            url: null,
          },
        }));
        console.log("unlike state set");
      })
      .catch((error) => console.log(error));
  }

  handlePostLike(e) {
    if (e.detail === 2) {
      this.handleLike(e);
    }
  }

  handleSub(e) {
    // e.textContent
    // const sparsh = document.getElementById("sparsh");
    const textEntered = this.state.value;
    console.log(textEntered, 'boom');
    const commentText = { text: textEntered };
    fetch(`/api/v1/comments/?postid=${this.state.postid}`, {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(commentText),
    })
      .then((response) => response.json())
      .then((data) => {
        this.setState((prevState) => ({
          comments: prevState.comments.concat(data),
        }));
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
      e.preventDefault();

    // sparsh.reset()
  }

  handleCha(e) {
    console.log("Here handleCha");
    this.setState({value: e.target.value});
  }

  render() {
    console.log("render ran");

    const {
      ownerImgUrl,
      owner,
      ownerShowUrl,
      postShowUrl,
      imgUrl,
      created,
      likes,
      comments,
    } = this.state;
    const dateToFormat = created;
    const { lognameLikesThis, numLikes } = likes;
    console.log("numlikes render click: ", numLikes);
    console.log("lognamelikesthis render click: ", lognameLikesThis);
    // const handleClick = lognameLikesThis === false ? this.handleLike : this.handleUnlike;
    //let timestamp = moment.utc(dateToFormat);
    const timestamp = moment(created).fromNow(true);
    return (
      <div>
        <a href={ownerShowUrl}>
          {" "}
          <img src={ownerImgUrl} alt="post-pic" />{" "}
        </a>
        <a href={ownerShowUrl}> {owner} </a>
        <a href={postShowUrl}>
          <p> {timestamp} ago</p>
        </a>
        <img src={imgUrl} alt="post-pic" id="postimg" />
        {/* onClick={this.handlePostLike} /> */}
        <Likes
          lognameLikesThis={lognameLikesThis}
          numLikes={numLikes}
          handleClickLike={this.handleLike}
          handleClickUnlike={this.handleUnlike}
        />
        {/* <CommentSection 
          comments={comments} /> */}
        <CommentForm 
        comments={comments} 
        value={this.state.value}
        handleSub={this.handleSub}
        handleCha={this.handleCha}/>
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
