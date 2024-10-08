/* ============================================================================
 * Copyright (c) Palo Alto Networks
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 * ========================================================================== */

import React from "react";

import CodeBlock from "@theme/CodeBlock";
import SchemaTabs from "@theme/SchemaTabs";
import TabItem from "@theme/TabItem";
/* eslint-disable import/no-extraneous-dependencies*/
import clsx from "clsx";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

import { createDescription } from "../../markdown/createDescription";
import { getQualifierMessage, getSchemaName } from "../../markdown/schema";
import { guard, toString } from "../../markdown/utils";

interface Map<T> {
  [key: string]: T;
}

export interface ExampleObject {
  summary?: string;
  description?: string;
  value?: any;
  externalValue?: string;
}

export interface Props {
  param: {
    description: string;
    example: any;
    examples: Map<ExampleObject>;
    name: string;
    required: boolean;
    deprecated: boolean;
    schema: any;
    enumDescriptions?: [string, string][];
  };
}

const getEnumDescriptionMarkdown = (enumDescriptions?: [string, string][]) => {
  if (enumDescriptions?.length) {
    return `| Enum Value | Description |
| ---- | ----- |
${enumDescriptions
  .map((desc) => {
    return `| ${desc[0]} | ${desc[1]} | `.replaceAll("\n", "<br/>");
  })
  .join("\n")}
    `;
  }

  return "";
};

function ParamsItem({ param, ...rest }: Props) {
  const {
    description,
    example,
    examples,
    name,
    required,
    deprecated,
    enumDescriptions,
  } = param;

  let schema = param.schema;
  let defaultValue: string | undefined;

  if (!schema || !schema?.type) {
    schema = { type: "any" };
  }
  if (schema) {
    if (schema.items) {
      defaultValue = schema.items.default;
    } else {
      defaultValue = schema.default;
    }
  }

  const renderSchemaName = guard(schema, (schema) => (
    <span className="openapi-schema__type"> {getSchemaName(schema)}</span>
  ));

  const renderSchemaRequired = guard(required, () => (
    <span className="openapi-schema__required">required</span>
  ));

  const renderDeprecated = guard(deprecated, () => (
    <span className="openapi-schema__deprecated">deprecated</span>
  ));

  const renderSchema = guard(getQualifierMessage(schema), (message) => (
    <div>
      <ReactMarkdown
        children={createDescription(message)}
        rehypePlugins={[rehypeRaw]}
      />
    </div>
  ));

  const renderDescription = guard(description, (description) => (
    <div>
      <ReactMarkdown
        children={createDescription(description)}
        components={{
          pre: "div",
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || "");
            if (inline) return <code>{children}</code>;
            return !inline && match ? (
              <CodeBlock className={className}>{children}</CodeBlock>
            ) : (
              <CodeBlock>{children}</CodeBlock>
            );
          },
        }}
        rehypePlugins={[rehypeRaw]}
      />
    </div>
  ));

  const renderEnumDescriptions = guard(
    getEnumDescriptionMarkdown(enumDescriptions),
    (value) => {
      return (
        <ReactMarkdown
          rehypePlugins={[rehypeRaw]}
          remarkPlugins={[remarkGfm]}
          children={value}
        />
      );
    }
  );

  function renderDefaultValue() {
    if (defaultValue !== undefined) {
      if (typeof defaultValue === "string") {
        return (
          <div>
            <strong>Default value: </strong>
            <span>
              <code>{defaultValue}</code>
            </span>
          </div>
        );
      }
      return (
        <div>
          <strong>Default value: </strong>
          <span>
            <code>{JSON.stringify(defaultValue)}</code>
          </span>
        </div>
      );
    }
    return undefined;
  }

  const renderExample = guard(toString(example), (example) => (
    <div>
      <strong>Example: </strong>
      {example}
    </div>
  ));

  const renderExamples = guard(examples, (examples) => {
    const exampleEntries = Object.entries(examples);
    return (
      <>
        <strong>Examples:</strong>
        <SchemaTabs>
          {exampleEntries.map(([exampleName, exampleProperties]) => (
            // @ts-ignore
            <TabItem value={exampleName} label={exampleName}>
              {exampleProperties.summary && <p>{exampleProperties.summary}</p>}
              {exampleProperties.description && (
                <p>
                  <strong>Description: </strong>
                  <span>{exampleProperties.description}</span>
                </p>
              )}
              <p>
                <strong>Example: </strong>
                <code>{exampleProperties.value}</code>
              </p>
            </TabItem>
          ))}
        </SchemaTabs>
      </>
    );
  });

  return (
    <div className="openapi-params__list-item">
      <span className="openapi-schema__container">
        <strong
          className={clsx("openapi-schema__property", {
            "openapi-schema__strikethrough": deprecated,
          })}
        >
          {name}
        </strong>
        {renderSchemaName}
        {(required || deprecated) && (
          <span className="openapi-schema__divider"></span>
        )}
        {renderSchemaRequired}
        {renderDeprecated}
      </span>
      {renderSchema}
      {renderDescription}
      {renderEnumDescriptions}
      {renderDefaultValue()}
      {renderExample}
      {renderExamples}
    </div>
  );
}

export default ParamsItem;