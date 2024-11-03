"""
create_wallets_table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            uid UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            amount NUMERIC CHECK (amount >= 0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    """,
        """
        DROP TABLE IF EXISTS wallets;
        """
    ),

    step(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """,
        """
        DROP FUNCTION IF EXISTS update_updated_at_column;
        """
    ),

    step(
        """
        CREATE TRIGGER update_wallet_updated_at
        BEFORE UPDATE ON wallets
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """,
        """
        DROP TRIGGER IF EXISTS update_wallet_updated_at ON wallets;
        """
    )
]
