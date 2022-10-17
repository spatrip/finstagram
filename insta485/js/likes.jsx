import React from "react";

// function Likes(props) {
//     const { numLikes, lognameLikesThis } = props;
//     let likeButton;
//     if (lognameLikesThis) {
//       likeButton = (
//         <button
//           type="button"
//           className="like-unlike-button"
//         onClick={handleClick}
//         >
//           Unlike
//         </button>
//       );
//     } else {
//       likeButton = (
//         <button
//           type="button"
//           className="like-unlike-button"
//         onClick={handleClick}
//         >
//           Like
//         </button>
//       );
//     }
//     console.log("number likes: ", numLikes);
//     console.log("logname likes: ", lognameLikesThis);
//     let likeText;
//     if (numLikes === 0 || numLikes > 1) {
//       likeText = <p> {numLikes} likes</p>;
//     } else {
//       likeText = <p> {numLikes} like </p>;
//     }
//     return (
//       <div>
//         {likeText}
//         {likeButton}
//       </div>
//     );
//   }

// Likes.propTypes = {
//   numLikes: PropTypes.number,
//   lognameLikesThis: PropTypes.bool,
// };

// export default Likes;
// const { isConstructorDeclaration } = require("typescript");

class Likes extends React.Component {
  constructor(props) {
    super(props);
    this.handleL = this.handleL.bind(this);
    this.handleUL = this.handleUL.bind(this);
    // this.state = { numLikes: 0, lognameLikesThis: '' };
  }

  handleL(e) {
    this.props.handleClickLike(e);
    // console.log("Like button clicked")
  }

  handleUL(e) {
    this.props.handleClickUnlike(e);
    // console.log("unlike button clicked")
  }

  render() {
    const numLikes = this.props.numLikes;
    const lognameLikesThis = this.props.lognameLikesThis;
    // const { numLikes, lognameLikesThis } = props;
    const likeText =
      this.props.numlikes === 0 || this.props.numLikes > 1 ? "likes" : "like";
    const likeButton =
      lognameLikesThis === true ? (
        <button
          type="button"
          onClick={this.handleUL}
          className="like-unlike-button"
        >
          Unlike
        </button>
      ) : (
        <button
          type="button"
          onClick={this.handleL}
          className="like-unlike-button"
        >
          Like
        </button>
      );
    // const whichButton = lognameLikesThis === true ? true : false; // dont need this
    return (
      <div>
        <p>
          {numLikes} {likeText}
        </p>
        <p>{likeButton}</p>
      </div>
    );
  }
}

export default Likes;
