defmodule Bballguesser.Team do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:name, :string, autogenerate: false}
  @foreign_key_type :string

  schema "teams" do
    field :conference, :string
    field :division, :string
    field :logo_url, :string

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(team, attrs) do
    team
    |> cast(attrs, [:name, :conference, :division, :logo_url])
    |> validate_required([:name, :conference, :division, :logo_url])
  end
end
