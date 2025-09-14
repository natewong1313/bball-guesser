defmodule Bballguesser.Repo do
  use Ecto.Repo,
    otp_app: :bballguesser,
    adapter: Ecto.Adapters.Postgres
end
