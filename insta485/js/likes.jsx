// import React from "react";

// class Likes extends React.Component {
//   render() {
//     const numLikes = this.props.numLikes;
//     const lognameLikesThis = this.props.lognameLikesThis;

//     //let likeText = "";

//     const likeText = numlikes === 0 || numLikes > 1 ? "likes" : "like";

//       if (numLikes === 0 || numLikes > 1) {
//       likeText = <p>{numLikes} likes</p> "likes";
//     } else {
//       likeText = "like";
//     }

//     let likeButton;
//     if (lognameLikesThis) {
//       likeButton = <button type="button">Unlike</button>;
//     }
//     else {
//         likeButton = <button type="button">Like</button>;
//     }
//     return (
//       <p>
//         {numLikes} {likeText}
//       </p>

//     );
//   }
// }
