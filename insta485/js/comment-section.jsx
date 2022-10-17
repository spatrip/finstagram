// import { resetWarningCache } from "prop-types";
import React from "react";
import Comment from "./comment";

// export default function CommentSection(props) {
//     const { comments } = props;
//     return (
//       <div>
//         {comments.map((comment) => (
//           <Comment owner={comment.owner} text={comment.text} />
//         ))}
//         {/* <form className="comment-form">
//           <input type="text" name="text" required />
//           <input type="submit" name="comment" value="comment" />
//         </form> */}
//       </div>
//     );
// }

// CommentSection.propTypes = {
//   comments: PropTypes.arrayOf,
// };

// value = "";
class CommentForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }

  // commentSection(props) {
  //   const { comments } = props;
  //   return (

  //   );

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleSubmit(event) {
    this.props.handleSub(event);
  }

  handleDelete(e) {
    this.props.deleteComment(e);
  }

  render() {
    const { comments } = this.props;
    // const deleteButton = <button type="button" onClick={this.handleDelete} className="delete-button">Delete</button>

    return (
      <div>
        {comments.map((comment) => (
          <Comment owner={comment.owner} text={comment.text} />
          // <b>
          //   {comment.lognameOwnsThis ? {deleteButton} : ''}
          // </b>
        ))}
        <form onSubmit={this.handleSubmit}>
          <label>
            <input
              type="text"
              value={this.state.value}
              onChange={this.handleChange}
              id="sparsh"
              className="comment-form"
            />
          </label>
        </form>
      </div>
    );
  }
}

export default CommentForm;
// // Comment.propTypes = {
//   owner: PropTypes.string,
//   text: PropTypes.string,
// };
