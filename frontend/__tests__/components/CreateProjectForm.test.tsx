/** Tests for CreateProjectForm: validation and successful submission. */

import { fireEvent, render, screen, waitFor } from "@testing-library/react";

// Mock the API barrel so no real network calls happen.
jest.mock("@/lib/api", () => ({
  projectsApi: {
    createProject: jest.fn(),
  },
}));

import { projectsApi } from "@/lib/api";
import { CreateProjectForm } from "@/components/projects/CreateProjectForm";

const createProjectMock = projectsApi.createProject as jest.Mock;

describe("CreateProjectForm", () => {
  afterEach(() => jest.clearAllMocks());

  it("shows an error when submitted with an empty name", async () => {
    render(<CreateProjectForm onCreated={jest.fn()} />);
    fireEvent.click(screen.getByText("Create project"));
    expect(await screen.findByText("Name is required")).toBeInTheDocument();
    expect(createProjectMock).not.toHaveBeenCalled();
  });

  it("creates a project and calls onCreated on success", async () => {
    const created = { id: 1, name: "Apollo", description: "", created_at: "", updated_at: "" };
    createProjectMock.mockResolvedValue(created);
    const onCreated = jest.fn();

    render(<CreateProjectForm onCreated={onCreated} />);
    fireEvent.change(screen.getByLabelText("Project name"), {
      target: { value: "Apollo" },
    });
    fireEvent.click(screen.getByText("Create project"));

    await waitFor(() => expect(onCreated).toHaveBeenCalledWith(created));
    expect(createProjectMock).toHaveBeenCalledWith({
      name: "Apollo",
      description: "",
    });
  });
});
