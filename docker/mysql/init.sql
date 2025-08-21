-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id          VARCHAR(36)  NOT NULL PRIMARY KEY,
    topic       VARCHAR(255) NOT NULL DEFAULT '',
    stance      LONGTEXT     NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    message_role    ENUM('user', 'model') NOT NULL,
    content         LONGTEXT NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_messages_conversation 
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) 
        ON DELETE CASCADE,
    KEY ix_messages_conv_id (conversation_id),
    KEY ix_messages_conv_id_id (conversation_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
