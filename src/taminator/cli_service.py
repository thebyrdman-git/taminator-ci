#!/usr/bin/env python3
"""
Taminator Service CLI Entry Point

Handles command-line arguments and launches the FastAPI service.
"""

import sys
import argparse
import logging
import uvicorn

def main():
    """Main entry point for the service"""
    parser = argparse.ArgumentParser(
        description="Taminator API Service v2.0 - Professional TAM Automation"
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8765,
        help='Port to listen on (default: 8765)'
    )
    parser.add_argument(
        '--log-level',
        default='info',
        choices=['debug', 'info', 'warning', 'error'],
        help='Log level (default: info)'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload (development only)'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='[%(asctime)s] %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Taminator API Service v2.0")
    logger.info(f"📡 Listening on http://{args.host}:{args.port}")
    logger.info(f"📚 API docs at http://{args.host}:{args.port}/docs")
    
    # Run the service
    try:
        uvicorn.run(
            "taminator.api.main:app",
            host=args.host,
            port=args.port,
            log_level=args.log_level,
            reload=args.reload,
            access_log=False  # Reduce noise
        )
    except KeyboardInterrupt:
        logger.info("🛑 Service stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Service crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


