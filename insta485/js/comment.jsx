import React from "react"

function Comment(props) {
  const { owner, text, lognameOwnsThis, commentid } = props;
  return (
    <>
      <p>
        <b>{owner}</b>
      </p>{" "}
      <p>{text}</p>
    </>
  );
}
export default Comment;