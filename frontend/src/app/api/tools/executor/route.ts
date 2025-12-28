import { NextRequest, NextResponse } from 'next/server'
import { executeToolCall } from '@/lib/tools/executor'

export async function POST(req: NextRequest) {
  try {
    const { tool, arguments: args } = await req.json()

    if (!tool) {
      return NextResponse.json(
        { error: 'Tool name is required' },
        { status: 400 }
      )
    }

    const result = await executeToolCall(tool, args || {})

    return NextResponse.json(result)
  } catch (error) {
    console.error('Tool executor error:', error)
    return NextResponse.json(
      { error: 'Failed to execute tool' },
      { status: 500 }
    )
  }
}
