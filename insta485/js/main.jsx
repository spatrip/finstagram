// preventing warnings: fix later
/* eslint-disable react/prop-types */
/* eslint-disable react/prefer-stateless-function */
/* eslint-disable max-classes-per-file */

import React from "react";
import { createRoot } from "react-dom/client";
// import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

class Feed extends React.Component {
  constructor(props) {
    super(props);
    this.state = { posts: [], nextPost: "" };
  }

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
        console.log("**********");
        console.log(data.next);
        console.log("********");
        this.setState({
          posts: data.results,
          nextPost: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  fetchNext() {
    console.log("=============");
    console.log(this.state);
    console.log("=============");
    const { nextPost } = this.state;
    fetch(nextPost, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log("---------------");
        console.log("next", data);
        console.log("---------------");
        this.setState((prevState) => ({
          posts: prevState.posts.concat(data.results),
          nextPost: data.next,
        }));
      })
      .catch((error) => console.log(error));
  }

  render() {
    console.log("!=============");
    console.log(this.state);
    console.log("!=============");
    const { posts, nextPost } = this.state;

    return (
      <div>
        <InfiniteScroll
          dataLength={posts.length}
          next={this.fetchNext}
          hasMore={nextPost !== ""}
          loader={<h4>Loading...</h4>}
          //endMessage={<p> End of feed </p>}
        >
          {posts.map((post) => (
            <div>
              <Post url={post.url} />
            </div>
          ))}
        </InfiniteScroll>
      </div>
    );
  }

  /* render() {
    const { posts } = this.state;
    return (
      <div>
        {posts.map((post) => (
          <div>
            <Post url={post.url} />
          </div>
        ))}
      </div>
    );
  } */
}

// Create a root
const root = createRoot(document.getElementById("reactEntry"));
// This method is only called once
// Insert the post component into the DOM

root.render(<Feed url="/api/v1/posts/" />);
