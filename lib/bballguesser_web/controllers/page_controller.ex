defmodule BballguesserWeb.PageController do
  use BballguesserWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
