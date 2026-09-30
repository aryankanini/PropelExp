"""Stable module entrypoint for the composed FastAPI application."""

from cms_planner.app import app, create_app

__all__ = ["app", "create_app"]