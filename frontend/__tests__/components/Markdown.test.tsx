/** Tests for the Markdown wrapper component.
 *
 * react-markdown/remark-gfm are mapped to mocks in jest.config.js, so this
 * verifies our wrapper renders content inside the expected container. */

import { render, screen } from "@testing-library/react";

import { Markdown } from "@/components/common/Markdown";

describe("Markdown", () => {
  it("renders its content inside a .markdown container", () => {
    const { container } = render(<Markdown>{"**hello**"}</Markdown>);
    expect(screen.getByText("**hello**")).toBeInTheDocument();
    expect(container.querySelector(".markdown")).not.toBeNull();
  });
});
