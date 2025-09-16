defmodule Bballguesser.Repo.Migrations.CreatePlayers do
  use Ecto.Migration

  def change do
    create table(:players, primary_key: false) do
      add :name, :string, primary_key: true
      add :positions, {:array, :string}
      add :age, :integer
      add :height, :integer
      add :number, :integer
      add :image_url, :string
      add :school, :string
      add :team_name, references(:teams, column: :name, type: :string, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:players, [:team_name])
  end
end
