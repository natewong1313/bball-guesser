defmodule Bballguesser.Player do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:name, :string, autogenerate: false}
  @foreign_key_type :string

  schema "players" do
    field :positions, {:array, :string}
    field :age, :integer
    field :height, :integer
    field :number, :integer
    field :school, :string
    field :image_url, :string
    field :team_name, :string

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(player, attrs) do
    player
    |> cast(attrs, [:name, :positions, :age, :height, :number, :school, :image_url])
    |> validate_required([:name, :positions, :age, :height, :number, :school, :image_url])
  end
end
